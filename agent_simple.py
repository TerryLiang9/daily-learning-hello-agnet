"""
智能旅行助手 - 简化版（仅天气查询）
不依赖 Tavily API，适合快速测试
"""
import re
import os
from dotenv import load_dotenv

from llm_client import OpenAICompatibleClient
from tools import get_weather

# 加载环境变量
load_dotenv()


# ============================================================================
# 智能体系统提示词（简化版）
# ============================================================================
AGENT_SYSTEM_PROMPT = """
你是一个智能天气助手。你的任务是查询天气并给出建议。

# 可用工具:
- `get_weather(city: str)`: 查询指定城市的实时天气。

# 输出格式要求:
你的每次回复必须严格遵循以下格式，包含一对 Thought 和 Action：

Thought: [你的思考过程和下一步计划]
Action: [你要执行的具体行动]

Action 的格式必须是以下之一：
1. 调用工具：function_name(arg_name="arg_value")
2. 结束任务：Finish[最终答案]

# 重要提示:
- 每次只输出一对 Thought-Action
- Action 必须在同一行，不要换行
- 查询到天气后，给出出行建议（如晴天适合户外活动等）
- 当获取到天气信息后，使用 Action: Finish[最终答案] 格式结束

请开始吧！
"""


# ============================================================================
# 智能体主循环
# ============================================================================
def run_agent_simple(user_prompt: str, max_loops: int = 3):
    """
    运行简化版智能体（仅天气查询）

    Args:
        user_prompt: 用户的初始请求
        max_loops: 最大循环次数
    """
    # --- 1. 配置 LLM 客户端 ---
    API_KEY = os.environ.get("API_KEY")
    BASE_URL = os.environ.get("BASE_URL")
    MODEL_ID = os.environ.get("MODEL_ID")

    # 检查必要的环境变量
    if not all([API_KEY, BASE_URL, MODEL_ID]):
        print("❌ 错误: 请确保在 .env 文件中配置了 API_KEY, BASE_URL 和 MODEL_ID")
        print("\n提示：")
        print("1. 复制配置文件: cp .env.zhipu.example .env")
        print("2. 编辑 .env 文件，填入你的智谱 API Key")
        return

    llm = OpenAICompatibleClient(
        model=MODEL_ID,
        api_key=API_KEY,
        base_url=BASE_URL
    )

    # --- 2. 初始化 ---
    prompt_history = [f"用户请求: {user_prompt}"]

    print(f"👤 用户输入: {user_prompt}")
    print("=" * 60)

    # --- 3. 运行主循环 ---
    for i in range(max_loops):
        print(f"\n🔄 循环 {i+1}/{max_loops}\n")

        # 3.1. 构建 Prompt
        full_prompt = "\n".join(prompt_history)

        # 3.2. 调用 LLM 进行思考
        llm_output = llm.generate(full_prompt, system_prompt=AGENT_SYSTEM_PROMPT)

        # 截断多余的 Thought-Action 对
        match = re.search(
            r'(Thought:.*?Action:.*?)(?=\n\s*(?:Thought:|Action:|Observation:)|\Z)',
            llm_output,
            re.DOTALL
        )
        if match:
            truncated = match.group(1).strip()
            if truncated != llm_output.strip():
                llm_output = truncated
                print("ℹ️  已截断多余的 Thought-Action 对")

        print(f"🤖 模型输出:\n{llm_output}\n")
        prompt_history.append(llm_output)

        # 3.3. 解析并执行行动
        action_match = re.search(r"Action: (.*)", llm_output, re.DOTALL)
        if not action_match:
            observation = "错误: 未能解析到 Action 字段。请确保你的回复严格遵循 'Thought: ... Action: ...' 的格式。"
            observation_str = f"Observation: {observation}"
            print(f"⚠️  {observation_str}\n" + "=" * 60)
            prompt_history.append(observation_str)
            continue

        action_str = action_match.group(1).strip()

        # 检查是否完成任务
        if action_str.startswith("Finish"):
            try:
                final_answer = re.match(r"Finish\[(.*)\]", action_str).group(1)
                print(f"✅ 任务完成！")
                print(f"📝 最终答案: {final_answer}")
                return
            except AttributeError:
                print("⚠️  Finish 格式错误，应该是 Finish[答案]")
                return

        # 解析工具调用
        try:
            tool_name = re.search(r"(\w+)\(", action_str).group(1)
            args_str = re.search(r"\((.*)\)", action_str).group(1)
            kwargs = dict(re.findall(r'(\w+)="([^"]*)"', args_str))
        except (AttributeError, ValueError) as e:
            observation = f"错误: 无法解析工具调用 - {e}"
            observation_str = f"Observation: {observation}"
            print(f"⚠️  {observation_str}\n" + "=" * 60)
            prompt_history.append(observation_str)
            continue

        # 执行工具
        if tool_name == "get_weather":
            print(f"🔧 调用工具: {tool_name}({kwargs})")
            observation = get_weather(**kwargs)
        else:
            observation = f"错误: 简化版仅支持 get_weather 工具"

        # 3.4. 记录观察结果
        observation_str = f"Observation: {observation}"
        print(f"📊 {observation_str}\n" + "=" * 60)
        prompt_history.append(observation_str)

    print(f"\n⏱️  已达到最大循环次数 ({max_loops})，任务结束")


# ============================================================================
# 主程序入口
# ============================================================================
if __name__ == "__main__":
    import sys

    # 示例任务
    default_task = "你好，请帮我查询一下北京和上海的天气，并给我一些出行建议。"

    if len(sys.argv) > 1:
        if sys.argv[1] == "--interactive" or sys.argv[1] == "-i":
            print("\n🎉 欢迎使用智能天气助手（简化版）！")
            print("💡 输入 'quit' 或 'exit' 退出\n")

            while True:
                try:
                    user_input = input("\n👤 请输入你要查询的城市: ").strip()
                    if not user_input:
                        continue
                    if user_input.lower() in ['quit', 'exit', '退出']:
                        print("\n👋 再见！")
                        break
                    print("\n" + "=" * 60)
                    run_agent_simple(f"请查询{user_input}的天气并给出建议")
                except KeyboardInterrupt:
                    print("\n\n👋 检测到中断信号，退出程序")
                    break
        else:
            task = " ".join(sys.argv[1:])
            print("=" * 60)
            run_agent_simple(task)
    else:
        print("=" * 60)
        run_agent_simple(default_task)

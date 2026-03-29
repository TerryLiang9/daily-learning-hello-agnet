"""
智能旅行助手 - 完整实现
基于 Thought-Action-Observation 循环的智能体系统

作者：DataWhale
教程：从零开始构建智能体
"""
import re
import os
import sys
import io
from dotenv import load_dotenv

# 修复 Windows 终端编码问题
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from llm_client import OpenAICompatibleClient
from tools import available_tools

# 加载环境变量
load_dotenv()


# ============================================================================
# 智能体系统提示词
# ============================================================================
AGENT_SYSTEM_PROMPT = """
你是一个智能旅行助手。你的任务是分析用户的请求，并使用可用工具一步步地解决问题。

# 可用工具:
- `get_weather(city: str)`: 查询指定城市的实时天气。
- `get_attraction(city: str, weather: str)`: 根据城市和天气搜索推荐的旅游景点。

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
- 当收集到足够信息可以回答用户问题时，必须使用 Action: Finish[最终答案] 格式结束

请开始吧！
"""


# ============================================================================
# 智能体主循环
# ============================================================================
def run_agent(user_prompt: str, max_loops: int = 5):
    """
    运行智能体主循环

    Args:
        user_prompt: 用户的初始请求
        max_loops: 最大循环次数，防止无限循环
    """
    # --- 1. 配置 LLM 客户端 ---
    API_KEY = os.environ.get("API_KEY")
    BASE_URL = os.environ.get("BASE_URL")
    MODEL_ID = os.environ.get("MODEL_ID")
    TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY")

    # 检查必要的环境变量
    if not all([API_KEY, BASE_URL, MODEL_ID]):
        print("❌ 错误: 请确保在 .env 文件中配置了 API_KEY, BASE_URL 和 MODEL_ID")
        return

    if not TAVILY_API_KEY:
        print("⚠️  警告: 未配置 TAVILY_API_KEY，景点推荐功能将不可用")

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

        # 截断多余的 Thought-Action 对（模型可能会输出多对）
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
        if tool_name in available_tools:
            print(f"🔧 调用工具: {tool_name}({kwargs})")
            observation = available_tools[tool_name](**kwargs)
        else:
            observation = f"错误:未定义的工具 '{tool_name}'"

        # 3.4. 记录观察结果
        observation_str = f"Observation: {observation}"
        print(f"📊 {observation_str}\n" + "=" * 60)
        prompt_history.append(observation_str)

    print(f"\n⏱️  已达到最大循环次数 ({max_loops})，任务结束")


# ============================================================================
# 交互式对话模式
# ============================================================================
def interactive_mode():
    """
    交互式对话模式，允许用户持续提问
    """
    print("\n🎉 欢迎使用智能旅行助手！")
    print("💡 输入 'quit' 或 'exit' 退出\n")

    while True:
        try:
            user_input = input("\n👤 请输入您的需求: ").strip()

            if not user_input:
                continue

            if user_input.lower() in ['quit', 'exit', '退出']:
                print("\n👋 再见！感谢使用智能旅行助手")
                break

            print("\n" + "=" * 60)
            run_agent(user_input)

        except KeyboardInterrupt:
            print("\n\n👋 检测到中断信号，退出程序")
            break
        except Exception as e:
            print(f"\n❌ 发生错误: {e}")


# ============================================================================
# 主程序入口
# ============================================================================
if __name__ == "__main__":
    import sys

    # 检查命令行参数
    if len(sys.argv) > 1:
        if sys.argv[1] == "--interactive" or sys.argv[1] == "-i":
            # 交互式模式
            interactive_mode()
        else:
            # 直接运行指定任务
            task = " ".join(sys.argv[1:])
            print("=" * 60)
            run_agent(task)
    else:
        # 默认任务
        default_task = "你好，请帮我查询一下今天北京的天气，然后根据天气推荐一个合适的旅游景点。"
        run_agent(default_task)

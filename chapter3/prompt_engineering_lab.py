"""
提示工程实验室
==============

对比不同提示策略对LLM输出效果的影响:
1. Zero-shot vs Few-shot
2. 思维链(CoT)
3. 角色扮演
4. 采样参数调优

需要配置: 在.env文件中设置API_KEY,或直接在代码中传入

作者: DataWhale Hello-Agents学习项目
"""

import os
import sys
from pathlib import Path
from typing import List, Dict, Any
import json

# 添加父目录到路径以导入llm_client
sys.path.insert(0, str(Path(__file__).parent.parent / 'chapter1'))

try:
    from llm_client import OpenAICompatibleClient
except ImportError:
    print("警告: 无法导入llm_client,请确保chapter1/llm_client.py存在")
    print("将使用模拟模式...")
    OpenAICompatibleClient = None


class PromptEngineeringLab:
    """提示工程实验室"""

    def __init__(self, api_key: str = None, base_url: str = None, model: str = None):
        """
        初始化实验室
        Args:
            api_key: API密钥
            base_url: API基础URL
            model: 模型名称
        """
        if OpenAICompatibleClient and api_key:
            self.client = OpenAICompatibleClient(
                model=model or "gpt-3.5-turbo",
                api_key=api_key,
                base_url=base_url or "https://api.openai.com/v1"
            )
            self.use_mock = False
        else:
            self.client = None
            self.use_mock = True
            print("使用模拟模式(不会实际调用API)")

    def _call_model(self, user_prompt: str, system_prompt: str = "You are a helpful assistant.",
                   temperature: float = 0.7, max_tokens: int = 500) -> str:
        """调用模型"""
        if self.use_mock:
            return self._mock_response(user_prompt, system_prompt)
        else:
            return self.client.generate(
                prompt=user_prompt,
                system_prompt=system_prompt
            )

    def _mock_response(self, user_prompt: str, system_prompt: str) -> str:
        """模拟响应(用于测试)"""
        return f"[模拟响应] 系统: {system_prompt[:50]}... 用户: {user_prompt[:50]}..."

    def compare_zero_shot_vs_few_shot(self, task: str, examples: List[Dict[str, str]] = None):
        """
        实验1: Zero-shot vs Few-shot对比
        Args:
            task: 任务描述
            examples: Few-shot示例 [{"input": ..., "output": ...}, ...]
        """
        print("=" * 60)
        print("实验1: Zero-shot vs Few-shot对比")
        print("=" * 60)
        print()

        # 默认示例:情感分类
        if examples is None:
            examples = [
                {"input": "这家餐厅的服务太慢了,食物也很一般。", "output": "负面"},
                {"input": "这部电影的情节很平淡,没什么亮点。", "output": "中性"},
                {"input": "我喜欢这个产品,质量很好,物流也快!", "output": "正面"},
            ]

        test_input = "Datawhale的AI Agent课程非常棒,我学到了很多!"

        print(f"任务: 情感分类")
        print(f"测试输入: {test_input}\n")

        # Zero-shot
        print("【Zero-shot提示】")
        zero_shot_prompt = f"""请判断以下文本的情感色彩(正面/负面/中性):

文本: {test_input}
情感:"""

        print("提示词:")
        print(zero_shot_prompt)
        print()
        zero_shot_response = self._call_model(zero_shot_prompt)
        print(f"模型回答: {zero_shot_response}")
        print()

        # Few-shot
        print("【Few-shot提示】")
        few_shot_prompt = "请判断以下文本的情感色彩(正面/负面/中性):\n\n"
        for ex in examples:
            few_shot_prompt += f"文本: {ex['input']}\n"
            few_shot_prompt += f"情感: {ex['output']}\n\n"

        few_shot_prompt += f"文本: {test_input}\n"
        few_shot_prompt += "情感:"

        print("提示词:")
        print(few_shot_prompt)
        print()
        few_shot_response = self._call_model(few_shot_prompt)
        print(f"模型回答: {few_shot_response}")
        print()

        print("【分析】")
        print("Zero-shot: 直接指令,依赖模型的预训练知识")
        print("Few-shot: 提供示例,帮助模型理解任务格式和期望")
        print()

    def compare_chain_of_thought(self, problem: str):
        """
        实验2: 思维链(CoT)提示
        Args:
            problem: 需要推理的问题
        """
        print("=" * 60)
        print("实验2: 思维链(CoT)提示")
        print("=" * 60)
        print()

        # 默认问题:数学计算
        if problem is None:
            problem = """一个篮球队在一个赛季的80场比赛中赢了60%。在接下来的赛季中,
他们打了15场比赛,赢了12场。两个赛季的总胜率是多少?"""

        print(f"问题: {problem}\n")

        # 直接提示
        print("【直接提示】")
        direct_prompt = f"""请回答以下问题:

{problem}

答案:"""

        print("提示词:")
        print(direct_prompt)
        print()
        direct_response = self._call_model(direct_prompt)
        print(f"模型回答: {direct_response}")
        print()

        # 思维链提示
        print("【思维链提示】")
        cot_prompt = f"""请回答以下问题。请一步一步地思考并解答。

{problem}

请一步一步地思考并解答。"""

        print("提示词:")
        print(cot_prompt)
        print()
        cot_response = self._call_model(cot_prompt)
        print(f"模型回答: {cot_response}")
        print()

        print("【分析】")
        print("直接提示: 可能直接给出答案,容易出错")
        print("思维链: 引导模型逐步推理,提高准确性")
        print()

    def compare_role_playing(self, question: str, role: str):
        """
        实验3: 角色扮演提示
        Args:
            question: 问题
            role: 角色描述
        """
        print("=" * 60)
        print("实验3: 角色扮演提示")
        print("=" * 60)
        print()

        if question is None:
            question = "请解释Python中的GIL(全局解释器锁)是什么?"

        if role is None:
            role = "一位资深的Python编程专家"

        print(f"问题: {question}\n")

        # 无角色
        print("【无角色提示】")
        no_role_prompt = f"""{question}"""

        print("提示词:")
        print(no_role_prompt)
        print()
        no_role_response = self._call_model(no_role_prompt)
        print(f"模型回答: {no_role_response[:200]}...")
        print()

        # 有角色
        print("【角色扮演提示】")
        role_prompt = f"""你现在是一位资深的Python编程专家。

{question}

要让一个初学者也能听懂。"""

        print("提示词:")
        print(role_prompt)
        print()
        role_response = self._call_model(role_prompt)
        print(f"模型回答: {role_response[:200]}...")
        print()

        print("【分析】")
        print("无角色: 回答可能过于技术化或不够专业")
        print("角色扮演: 设定专家身份,引导输出风格和深度")
        print()

    def compare_temperature(self, prompt: str, temperatures: List[float] = None):
        """
        实验4: 温度参数对比
        Args:
            prompt: 输入提示
            temperatures: 温度值列表
        """
        print("=" * 60)
        print("实验4: 温度参数对比")
        print("=" * 60)
        print()

        if prompt is None:
            prompt = "请写一个关于人工智能的简短介绍。"

        if temperatures is None:
            temperatures = [0.1, 0.7, 1.5]

        print(f"提示: {prompt}\n")

        for temp in temperatures:
            print(f"【Temperature = {temp}】")

            if self.use_mock:
                response = f"[模拟响应] T={temp}: " + {
                    0.1: "输出稳定、确定性强,重复度高",
                    0.7: "输出平衡、自然,有一定创造性",
                    1.5: "输出多样、创新,可能不太连贯"
                }.get(temp, "中等多样性")
            else:
                # 实际调用时传入temperature参数
                response = self._call_model(prompt, temperature=temp)

            print(f"响应: {response[:150]}...")
            print()

        print("【分析】")
        print("低温度(0.1): 输出保守、确定,适合事实性任务")
        print("中温度(0.7): 输出平衡、自然,适合日常对话")
        print("高温度(1.5): 输出多样、创新,适合创意写作")
        print()

    def run_all_experiments(self):
        """运行所有实验"""
        print("\n")
        print("█" * 60)
        print("█" + " " * 20 + "提示工程实验室" + " " * 20 + "█")
        print("█" * 60)
        print("\n")

        # 实验1
        self.compare_zero_shot_vs_few_shot(None)
        input("按Enter继续下一个实验...")

        # 实验2
        self.compare_chain_of_thought(None)
        input("按Enter继续下一个实验...")

        # 实验3
        self.compare_role_playing(None, None)
        input("按Enter继续下一个实验...")

        # 实验4
        self.compare_temperature(None, None)

        print("=" * 60)
        print("所有实验完成!")
        print("=" * 60)


def main():
    """主函数"""
    # 从环境变量读取配置
    api_key = os.getenv('API_KEY')
    base_url = os.getenv('BASE_URL')
    model_id = os.getenv('MODEL_ID')

    # 如果没有配置,使用模拟模式
    if not api_key:
        print("未检测到API配置,使用模拟模式")
        print("要使用真实API,请设置环境变量或.env文件:")
        print("  API_KEY=your_api_key")
        print("  BASE_URL=https://open.bigmodel.cn/api/paas/v4/")
        print("  MODEL_ID=glm-4-flash")
        print()

    lab = PromptEngineeringLab(api_key, base_url, model_id)

    # 运行所有实验
    lab.run_all_experiments()


if __name__ == '__main__':
    main()

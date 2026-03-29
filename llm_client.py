"""
智能旅行助手 - LLM 客户端模块
提供 OpenAI 兼容的大语言模型接口
"""
from openai import OpenAI


class OpenAICompatibleClient:
    """
    一个用于调用任何兼容OpenAI接口的LLM服务的客户端

    支持的服务商包括：
    - OpenAI 官方
    - Azure OpenAI
    - 国内兼容 OpenAI 接口的服务（如通义千问、文心一言等）
    - 本地部署的模型服务（如 Ollama、vLLM 等）
    """

    def __init__(self, model: str, api_key: str, base_url: str):
        """
        初始化 LLM 客户端

        Args:
            model: 模型名称或 ID，如 "gpt-3.5-turbo"
            api_key: API 密钥
            base_url: API 基础 URL
        """
        self.model = model
        self.client = OpenAI(api_key=api_key, base_url=base_url)

    def generate(self, prompt: str, system_prompt: str) -> str:
        """
        调用 LLM API 来生成回应

        Args:
            prompt: 用户提示词
            system_prompt: 系统提示词（定义智能体的角色和行为）

        Returns:
            str: LLM 生成的回应
        """
        print("正在调用大语言模型...")
        try:
            messages = [
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': prompt}
            ]
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                stream=False
            )
            answer = response.choices[0].message.content
            print("大语言模型响应成功。")
            return answer
        except Exception as e:
            print(f"调用LLM API时发生错误: {e}")
            return "错误:调用语言模型服务时出错。"


if __name__ == "__main__":
    # 测试 LLM 客户端
    # 注意：需要先配置环境变量

    import os
    from dotenv import load_dotenv

    # 加载环境变量
    load_dotenv()

    API_KEY = os.environ.get("API_KEY", "your_api_key_here")
    BASE_URL = os.environ.get("BASE_URL", "https://api.openai.com/v1")
    MODEL_ID = os.environ.get("MODEL_ID", "gpt-3.5-turbo")

    # 测试系统提示词
    test_system_prompt = "你是一个友好的助手。"

    # 测试客户端
    llm = OpenAICompatibleClient(
        model=MODEL_ID,
        api_key=API_KEY,
        base_url=BASE_URL
    )

    response = llm.generate(
        prompt="你好！请简单介绍一下自己。",
        system_prompt=test_system_prompt
    )

    print(f"\n模型回应:\n{response}")

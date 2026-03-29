# 🌍 智能旅行助手

> 基于 **Thought-Action-Observation** 循环的 AI 智能体实践项目

**教程来源**: [DataWhale - 从零开始构建智能体](https://github.com/datawhalechina/hello-agents)

---

## ✨ 项目简介

这是一个完整实现的智能旅行助手，展示了如何构建一个基于大语言模型（LLM）的智能体系统。智能体能够：

- 🌤️ **查询天气** - 实时获取任意城市的天气状况
- 🏛️ **推荐景点** - 根据天气条件智能推荐旅游景点
- 🤔 **自主决策** - 通过 Thought-Action-Observation 循环自主规划任务
- 🔄 **动态调整** - 根据环境反馈灵活调整策略

---

## 🎯 核心特性

### 1. Thought-Action-Observation 循环

```
┌─────────────┐
│  感知 Perception │
└──────┬──────┘
       ↓
┌─────────────┐
│  思考 Thought    │  ← LLM 进行推理和规划
└──────┬──────┘
       ↓
┌─────────────┐
│  行动 Action     │  ← 调用工具/执行操作
└──────┬──────┘
       ↓
┌─────────────┐
│  观察 Observation│  ← 获取环境反馈
└──────┬──────┘
       ↓
    （循环继续）
```

### 2. 支持的工具

| 工具名称 | 功能描述 | 数据源 |
|---------|---------|--------|
| `get_weather` | 查询城市实时天气 | [wttr.in](https://wttr.in) |
| `get_attraction` | 推荐旅游景点 | Tavily Search API |

---

## 🚀 快速开始

### 1. 安装依赖

```bash
# 使用 pip 安装
pip install -r requirements.txt

# 或使用 uv（更快）
uv pip install -r requirements.txt
```

### 2. 配置环境变量

**方式 A：使用智谱 AI（推荐）**

```bash
# 使用智谱 AI 配置模板
cp .env.zhipu.example .env
```

编辑 `.env` 文件：

```env
# 智谱 AI 配置
API_KEY=your_zhipu_api_key_here
BASE_URL=https://open.bigmodel.cn/api/anthropic
MODEL_ID=glm-4-flash

# Tavily 搜索 API（用于景点推荐）
TAVILY_API_KEY=your_tavily_api_key_here
```

**方式 B：使用其他兼容 OpenAI 的服务**

```bash
# 使用通用配置模板
cp .env.example .env
```

编辑 `.env` 文件：

**方案 A：使用智谱 AI（推荐）**

```env
# 智谱 AI 配置
API_KEY=your_zhipu_api_key_here
BASE_URL=https://open.bigmodel.cn/api/anthropic
MODEL_ID=glm-4-flash

# Tavily 搜索 API（用于景点推荐）
TAVILY_API_KEY=your_tavily_api_key_here
```

**方案 B：使用其他兼容 OpenAI 的服务**

```env
# OpenAI 配置（或兼容 OpenAI 接口的服务）
API_KEY=your_api_key_here
BASE_URL=https://api.openai.com/v1
MODEL_ID=gpt-3.5-turbo

# Tavily 搜索 API（用于景点推荐）
TAVILY_API_KEY=your_tavily_api_key_here
```

#### 🔑 获取 API 密钥

**⭐ 快速配置智谱 AI（推荐）：**

👉 查看 [智谱 AI 快速配置指南](./QUICKSTART_ZHIPU.md)

```bash
# 1. 访问获取 API Key: https://open.bigmodel.cn/
# 2. 复制配置模板
cp .env.zhipu.example .env
# 3. 编辑 .env 填入你的 API Key
# 4. 运行
python agent.py
```

**其他可选 LLM API：**
- [通义千问](https://dashscope.aliyun.com/)
- [DeepSeek](https://platform.deepseek.com/)
- [OpenAI 官方](https://platform.openai.com/api-keys)

**Tavily API（用于景点推荐）：**
- 访问 [Tavily 官网](https://www.tavily.com/) 注册
- 免费额度 1000 次/月

### 3. 运行智能体

```bash
# 方式 1: 运行默认任务
python agent.py

# 方式 2: 指定自定义任务
python agent.py "帮我查一下上海的天气，推荐一些适合雨天游玩的地方"

# 方式 3: 交互式对话模式
python agent.py --interactive
```

---

## 📁 项目结构

```
chapter1/
├── agent.py              # 主程序：智能体循环
├── llm_client.py         # LLM 客户端封装
├── tools.py              # 工具函数集合
├── requirements.txt      # Python 依赖
├── .env.example          # 环境变量模板
├── .gitignore           # Git 忽略文件
└── README.md            # 本文档
```

---

## 🔧 模块说明

### `llm_client.py` - LLM 客户端

提供统一的 OpenAI 兼容接口，支持：
- ✅ **智谱 AI**（GLM-4 系列，推荐）
- ✅ 通义千问、文心一言等国内服务
- ✅ OpenAI 官方 API
- ✅ 本地模型服务（Ollama、vLLM）

```python
from llm_client import OpenAICompatibleClient

# 使用智谱 AI
llm = OpenAICompatibleClient(
    model="glm-4-flash",
    api_key="your-zhipu-api-key",
    base_url="https://open.bigmodel.cn/api/anthropic"
)

# 或使用 OpenAI
llm = OpenAICompatibleClient(
    model="gpt-3.5-turbo",
    api_key="your-key",
    base_url="https://api.openai.com/v1"
)

response = llm.generate(
    prompt="你好",
    system_prompt="你是一个友好的助手"
)
```

### `tools.py` - 工具函数

包含两个核心工具：

```python
# 查询天气
get_weather("北京")  # → "北京当前天气:晴，气温26摄氏度"

# 推荐景点
get_attraction("北京", "晴天")  # → "推荐颐和园、长城..."
```

### `agent.py` - 主循环

实现完整的智能体循环：
1. **感知** - 接收用户输入和工具返回
2. **思考** - LLM 进行推理和规划
3. **行动** - 调用工具或完成任务
4. **观察** - 获取行动结果并反馈

---

## 📊 运行示例

```bash
$ python agent.py

👤 用户输入: 你好，请帮我查询一下今天北京的天气，然后根据天气推荐一个合适的旅游景点。
============================================================

🔄 循环 1/5

正在调用大语言模型...
大语言模型响应成功。
🤖 模型输出:
Thought: 首先需要获取北京今天的天气情况，之后再根据天气情况来推荐旅游景点。
Action: get_weather(city="北京")

🔧 调用工具: get_weather({'city': '北京'})
📊 Observation: 北京当前天气:Sunny，气温26摄氏度
============================================================

🔄 循环 2/5

正在调用大语言模型...
大语言模型响应成功。
🤖 模型输出:
Thought: 现在已经知道了北京今天的天气是晴朗且温度适中，接下来可以基于这个信息来推荐一个适合的旅游景点了。
Action: get_attraction(city="北京", weather="Sunny")

🔧 调用工具: get_attraction({'city': '北京', 'weather': 'Sunny'})
📊 Observation: 北京在晴天最值得去的旅游景点是颐和园...
============================================================

🔄 循环 3/5

正在调用大语言模型...
大语言模型响应成功。
🤖 模型输出:
Thought: 已经获得了两个适合晴天游览的景点建议，现在可以根据这些信息给用户提供满意的答复。
Action: Finish[今天北京的天气是晴朗的，气温26摄氏度，非常适合外出游玩。我推荐您去颐和园欣赏美丽的湖景和古建筑，或者前往长城体验其壮观的景观和深厚的历史意义。希望您有一个愉快的旅行！]

✅ 任务完成！
📝 最终答案: 今天北京的天气是晴朗的，气温26摄氏度，非常适合外出游玩。我推荐您去颐和园欣赏美丽的湖景和古建筑，或者前往长城体验其壮观的景观和深厚的历史意义。希望您有一个愉快的旅行！
```

---

## 🧪 测试工具函数

```bash
# 测试天气查询
python tools.py

# 测试 LLM 客户端
python llm_client.py
```

---

## 💡 扩展思路

基于当前框架，你可以轻松添加新功能：

### 1. 添加记忆功能

```python
# 在 tools.py 中添加
memory = {
    "preferences": [],  # 用户偏好
    "history": []        # 历史记录
}

def save_preference(preference: str) -> str:
    memory["preferences"].append(preference)
    return f"已记住您的偏好: {preference}"
```

### 2. 添加更多工具

```python
# 预订酒店
def book_hotel(city: str, check_in: str, check_out: str) -> str:
    # 调用酒店预订 API
    pass

# 查询交通
def get_traffic(from_city: str, to_city: str) -> str:
    # 调用交通查询 API
    pass
```

### 3. 添加反思能力

在主循环中添加反思步骤：

```python
# 每 3 次循环后进行反思
if (i + 1) % 3 == 0:
    reflection = llm.generate(
        prompt=f"历史记录: {prompt_history}\n请反思当前进展",
        system_prompt="你是一个反思者..."
    )
```

---

## 📚 学习资源

- 📖 [完整教程文档](https://github.com/datawhalechina/hello-agents/blob/main/docs/chapter1/)
- 💬 [GitHub Discussions](https://github.com/datawhalechina/hello-agents/discussions)
- 🎥 [视频教程](https://www.modelscope.cn/learn/6016)

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

## 📄 许可证

MIT License

---

## 🙏 致谢

本项目基于 [DataWhale](https://github.com/datawhalechina) 的《从零开始构建智能体》教程。

---

**祝你学习愉快！** 🎉

# DataWhale Hello-Agents 学习项目

> 从零开始构建智能体 - 系统学习笔记与实践项目

**教程来源**: [DataWhale - Hello-Agents](https://github.com/datawhalechina/hello-agents)

---

## 📚 项目结构

本仓库包含学习 DataWhale《从零开始构建智能体》教程的完整实践项目。

```
daily-learning-hello-agnet/
├── chapter1/              # 第一章：初识智能体
│   ├── agent.py          # 完整版智能旅行助手
│   ├── agent_simple.py   # 简化版（仅天气查询）
│   ├── llm_client.py     # LLM 客户端封装
│   ├── tools.py          # 工具函数集合
│   └── ...
├── chapter2/              # 第二章：（待添加）
├── chapter3/              # 第三章：（待添加）
└── README.md             # 本文档
```

---

## 🎯 第一章：初识智能体

**项目**: 智能旅行助手

基于 **Thought-Action-Observation** 循环的 AI 智能体实践项目，展示如何构建一个基于大语言模型（LLM）的智能体系统。

### 核心功能

- 🌤️ **查询天气** - 实时获取任意城市的天气状况
- 🏛️ **推荐景点** - 根据天气条件智能推荐旅游景点
- 🤔 **自主决策** - 通过 Thought-Action-Observation 循环自主规划任务
- 🔄 **动态调整** - 根据环境反馈灵活调整策略

### 技术栈

- 支持 **智谱 AI (GLM-4)**、OpenAI 等多种 LLM
- 兼容 OpenAI SDK 的统一接口
- 完整的配置示例和使用文档

### 快速开始

```bash
# 进入第一章目录
cd chapter1

# 安装依赖
pip install -r requirements.txt

# 配置 API Keys
cp .env.zhipu.example .env
# 编辑 .env 填入你的智谱 API Key 和 Tavily API Key

# 运行智能体
python agent.py  # 完整版
python agent_simple.py  # 简化版
```

### 详细文档

- 📖 [完整使用文档](./chapter1/README.md)
- 🚀 [智谱 AI 快速配置指南](./chapter1/QUICKSTART_ZHIPU.md)

---

## 📖 学习进度

| 章节 | 标题 | 状态 | 完成时间 |
|------|------|------|---------|
| 第一章 | 初识智能体 | ✅ 已完成 | 2026-03-29 |
| 第二章 | 智能体发展历史 | ⏳ 待完成 | - |
| 第三章 | 智能体的核心组件 | ⏳ 待完成 | - |
| 第四章 | 提示工程 | ⏳ 待完成 | - |
| 第五章 | 智能体记忆机制 | ⏳ 待完成 | - |
| 第六章 | 智能体规划能力 | ⏳ 待完成 | - |
| 第七章 | 智能体工具使用 | ⏳ 待完成 | - |

---

## 🛠️ 技术要求

- Python 3.8+
- 大语言模型 API（智谱 AI / OpenAI / 通义千问等）
- Tavily Search API（用于搜索功能）

---

## 📝 使用说明

每章的项目都是独立的，包含完整的代码和文档。建议按顺序学习：

1. 阅读 DataWhale 教程原文
2. 运行对应章节的代码
3. 理解核心概念和实现原理
4. 完成章末习题
5. 扩展实现自己的想法

---

## 🔗 相关资源

- 📚 [DataWhale Hello-Agents 教程](https://github.com/datawhalechina/hello-agents)
- 💬 [GitHub Discussions](https://github.com/datawhalechina/Hello-Agents/discussions)
- 🎥 [视频教程](https://www.modelscope.cn/learn/6016)

---

## 📄 许可证

MIT License

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

## 🙏 致谢

本项目基于 [DataWhale](https://github.com/datawhalechina) 的《从零开始构建智能体》教程。

---

**祝你学习愉快！** 🎉

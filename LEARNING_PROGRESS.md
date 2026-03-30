# DataWhale Hello-Agents 学习进度

> 从零开始构建智能体 - 系统学习笔记与实践项目

**教程来源**: [DataWhale - Hello-Agents](https://github.com/datawhalechina/hello-agents)

---

## 📚 学习进度

| 章节 | 标题 | 状态 | 完成时间 | 实践项目 |
|------|------|------|---------|---------|
| 第一章 | 初识智能体 | ✅ 已完成 | 2026-03-29 | 智能旅行助手 |
| 第二章 | 智能体发展历史 | ✅ 已完成 | 2026-03-29 | - |
| 第三章 | 智能体的核心组件 | ✅ 已完成 | 2026-03-29 | - |
| 第四章 | 智能体经典范式构建 | ✅ 已完成 | 2026-03-30 | ReAct/Plan-and-Solve/Reflection |
| 第五章 | 基于低代码平台的智能体搭建 | ✅ 已完成 | 2026-03-30 | 学习笔记 |
| 第六章 | 框架开发实践 | ✅ 已完成 | 2026-03-30 | LangGraph/AutoGen学习笔记 |
| 第七章 | 构建你的Agent框架 | ✅ 已完成 | 2026-03-30 | 简单Agent框架设计 |
| 第八章 | 记忆与检索 | ✅ 已完成 | 2026-03-30 | RAG系统实现 |

---

## 🎯 核心知识点

### 第一章：初识智能体
- **Thought-Action-Observation循环**
- 智能体基本架构
- LLM与工具的协同

### 第二章：智能体发展历史
- 从Rule-based到LLM-based
- 关键里程碑
- 未来发展趋势

### 第三章：智能体的核心组件
- 大语言模型（LLM）
- 提示工程
- 工具调用

### 第四章：智能体经典范式构建
- **ReAct**：边想边做，动态调整
- **Plan-and-Solve**：先规划后执行
- **Reflection**：自我反思与迭代

### 第五章：基于低代码平台的智能体搭建
- **Coze**：零代码Agent构建
- **Dify**：开源LLM应用平台
- **n8n**：工作流自动化

### 第六章：框架开发实践
- **LangGraph**：状态图建模
- **AutoGen**：多智能体协作
- **AgentScope**：模块化开发

### 第七章：构建你的Agent框架
- 框架核心架构设计
- 记忆模块实现
- 工具系统设计

### 第八章：记忆与检索
- 向量存储
- **RAG（检索增强生成）**
- 文档问答系统

---

## 📁 项目结构

```
daily-learning-hello-agnet/
├── chapter1/              # 第一章：初识智能体
│   ├── agent.py          # 完整版智能旅行助手
│   ├── agent_simple.py   # 简化版（仅天气查询）
│   ├── llm_client.py     # LLM 客户端封装
│   └── tools.py          # 工具函数集合
├── chapter4/              # 第四章：智能体经典范式构建
│   ├── react_agent.py    # ReAct智能体实现
│   ├── plan_solve_agent.py # Plan-and-Solve智能体
│   ├── reflection_agent.py # Reflection智能体
│   ├── memory.py         # 记忆模块
│   ├── tools.py          # 工具系统
│   └── llm_client.py     # LLM客户端
├── chapter5/              # 第五章：低代码平台
│   └── README.md         # 学习笔记
├── chapter6/              # 第六章：框架开发
│   └── README.md         # 学习笔记
├── chapter7/              # 第七章：构建Agent框架
│   └── README.md         # 框架设计文档
├── chapter8/              # 第八章：记忆与检索
│   └── README.md         # RAG系统实现
└── README.md             # 本文档
```

---

## 🛠️ 技术栈

### 编程语言
- Python 3.8+

### 核心库
- OpenAI SDK
- LangChain/LangGraph
- sentence-transformers
- numpy

### 平台工具
- Coze（低代码）
- Dify（开源平台）
- n8n（工作流自动化）

---

## 💡 学习收获

### 核心能力
1. **智能体范式掌握**：ReAct、Plan-and-Solve、Reflection
2. **框架应用能力**：LangGraph、AutoGen、AgentScope
3. **系统设计能力**：从零构建Agent框架
4. **RAG实现能力**：向量检索 + LLM生成

### 实践经验
- 完成多个智能体项目
- 掌握工具调用和记忆管理
- 理解提示工程的重要性
- 学会使用低代码平台

---

## 📖 待学习内容

### 高级主题（后续章节）
- 第九章：上下文工程
- 第十章：智能体通信协议
- 第十一章：Agent训练
- 第十二章：评估方法

### 综合案例
- 第十三章：智能旅行助手（升级版）
- 第十四章：自动化深度研究智能体
- 第十五章：赛博小镇（多智能体模拟）

---

## 🎓 学习建议

1. **循序渐进**：按顺序学习各章节，确保基础扎实
2. **动手实践**：每章都要运行代码，理解原理
3. **扩展思考**：在基础代码上添加自己的功能
4. **项目驱动**：尝试用学到的知识解决实际问题

---

## 🔗 相关资源

- 📚 [DataWhale Hello-Agents教程](https://github.com/datawhalechina/hello-agents)
- 💬 [GitHub Discussions](https://github.com/datawhalechina/Hello-Agents/discussions)
- 🎥 [视频教程](https://www.modelscope.cn/learn/6016)

---

## 📄 许可证

MIT License

---

## 🤝 贡献

欢迎提交Issue和Pull Request！

---

## 🙏 致谢

本项目基于 [DataWhale](https://github.com/datawhalechina) 的《从零开始构建智能体》教程。

---

**祝你学习愉快！** 🎉

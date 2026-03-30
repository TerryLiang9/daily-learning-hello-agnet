# DataWhale Hello-Agents 学习项目

> 从零开始构建智能体 - 系统学习笔记与实践项目

**教程来源**: [DataWhale - Hello-Agents](https://github.com/datawhalechina/hello-agents)

---

## 📚 项目简介

本仓库包含学习 DataWhale《从零开始构建智能体》教程的完整实践项目。通过理论学习与代码实践相结合的方式，系统掌握智能体开发的核心技术。

---

## 🎯 学习进度

| 章节 | 标题 | 状态 | 实践项目 |
|------|------|------|---------|
| 第一章 | 初识智能体 | ✅ 已完成 | 智能旅行助手 |
| 第二章 | 智能体发展历史 | ✅ 已完成 | - |
| 第三章 | 智能体的核心组件 | ✅ 已完成 | - |
| 第四章 | 智能体经典范式构建 | ✅ 已完成 | ReAct/Plan-and-Solve/Reflection |
| 第五章 | 基于低代码平台的智能体搭建 | ✅ 已完成 | 学习笔记 |
| 第六章 | 框架开发实践 | ✅ 已完成 | LangGraph/AutoGen |
| 第七章 | 构建你的Agent框架 | ✅ 已完成 | 框架设计文档 |
| 第八章 | 记忆与检索 | ✅ 已完成 | RAG系统 |

详细进度请查看 [LEARNING_PROGRESS.md](./LEARNING_PROGRESS.md)

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
│   └── tools.py          # 工具系统
├── chapter5/              # 第五章：低代码平台学习笔记
├── chapter6/              # 第六章：框架开发实践
├── chapter7/              # 第七章：构建Agent框架
├── chapter8/              # 第八章：记忆与检索
├── LEARNING_PROGRESS.md   # 学习进度详情
└── README.md             # 本文档
```

---

## 🛠️ 技术栈

- **Python 3.8+**
- **OpenAI SDK** - LLM接口
- **LangChain/LangGraph** - 框架开发
- **sentence-transformers** - 向量嵌入
- **numpy** - 数值计算

---

## 🚀 快速开始

### 第一章：智能旅行助手

```bash
cd chapter1

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 填入你的 API Keys

# 运行完整版智能体
python agent.py

# 运行简化版
python agent_simple.py
```

### 第四章：经典智能体范式

```bash
cd chapter4

# 安装依赖
pip install -r requirements.txt

# 配置环境变量（包括SerpApi密钥）
cp .env.example .env

# 运行ReAct智能体
python react_agent.py

# 运行Plan-and-Solve智能体
python plan_solve_agent.py

# 运行Reflection智能体
python reflection_agent.py
```

---

## 💡 核心知识点

### 智能体范式

1. **ReAct**：思考-行动-观察循环
   - 边想边做，动态调整
   - 适合探索性任务

2. **Plan-and-Solve**：先规划后执行
   - 结构化分解
   - 适合逻辑清晰的任务

3. **Reflection**：自我反思与优化
   - 迭代改进
   - 适合高质量要求

### 框架应用

- **LangGraph**：状态图建模
- **AutoGen**：多智能体协作
- **Coze/Dify**：低代码平台

### 高级技术

- **RAG**：检索增强生成
- **记忆系统**：工作记忆 + 长期记忆
- **工具调用**：扩展智能体能力

---

## 📖 学习路线

1. **基础入门**（第1-3章）
   - 理解智能体概念
   - 掌握LLM调用
   - 学习提示工程

2. **核心实践**（第4章）
   - 实现三种经典范式
   - 工具系统设计
   - 记忆管理

3. **框架应用**（第5-7章）
   - 低代码平台使用
   - 主流框架实践
   - 自研框架设计

4. **高级进阶**（第8章）
   - 向量检索
   - RAG系统
   - 问答系统

---

## 🎓 学习建议

1. **循序渐进**：按顺序学习各章节
2. **动手实践**：运行所有示例代码
3. **扩展思考**：在基础代码上添加功能
4. **项目驱动**：用所学知识解决实际问题

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

欢迎提交 Issue 和 Pull Request！

---

## 🙏 致谢

本项目基于 [DataWhale](https://github.com/datawhalechina) 的《从零开始构建智能体》教程。

---

**祝你学习愉快！** 🎉

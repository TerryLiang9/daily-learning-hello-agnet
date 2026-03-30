# 第四章：智能体经典范式构建

> 基于三种经典范式从零构建智能体系统

**本章实现**：
- ReAct（Reasoning and Acting）：思考-行动-观察循环
- Plan-and-Solve：先规划后执行
- Reflection：自我反思与迭代优化

---

## 环境准备

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

复制 `.env.example` 为 `.env` 并填入你的API密钥：

```bash
cp .env.example .env
```

需要配置的密钥：
- `LLM_API_KEY`：大语言模型API密钥
- `LLM_MODEL_ID`：模型ID（如 glm-4、gpt-4 等）
- `LLM_BASE_URL`：API服务地址
- `SERPAPI_API_KEY`：SerpApi搜索服务密钥（用于ReAct智能体）

### 3. 获取SerpApi密钥

- 访问 [SerpApi官网](https://serpapi.com/) 注册免费账户
- 获取API密钥并添加到 `.env` 文件

---

## 项目结构

```
chapter4/
├── llm_client.py          # LLM客户端封装
├── tools.py               # 工具定义与执行器
├── react_agent.py         # ReAct智能体实现
├── plan_solve_agent.py    # Plan-and-Solve智能体实现
├── reflection_agent.py    # Reflection智能体实现
├── memory.py              # 记忆模块（Reflection使用）
└── README.md              # 本文档
```

---

## 使用说明

### 1. ReAct智能体

回答需要实时信息的问题，通过搜索工具获取外部知识。

```bash
python react_agent.py
```

**示例问题**：
- 华为最新的手机是哪一款？它的主要卖点是什么？
- 英伟达最新的GPU型号是什么？

**核心特点**：
- 边想边做，动态调整
- 适合探索性任务
- 需要外部信息的场景

### 2. Plan-and-Solve智能体

将复杂问题先分解为计划，再逐步执行。

```bash
python plan_solve_agent.py
```

**示例问题**：
- 数学应用题（多步推理）
- 报告撰写任务
- 代码生成任务

**核心特点**：
- 三思而后行
- 结构化分解
- 适合逻辑链条清晰的任务

### 3. Reflection智能体

通过自我反思和迭代优化来提升输出质量。

```bash
python reflection_agent.py
```

**示例任务**：
- 代码生成与优化
- 算法实现改进
- 文本内容优化

**核心特点**：
- 执行-反思-优化循环
- 自动质量提升
- 适合对质量要求高的场景

---

## 三种范式对比

| 范式 | 核心思想 | 优势 | 适用场景 |
|------|----------|------|----------|
| ReAct | 边想边做 | 环境适应性强 | 需要外部工具、探索性任务 |
| Plan-and-Solve | 先规划后执行 | 结构稳定 | 多步推理、逻辑清晰的任务 |
| Reflection | 自我迭代 | 质量高 | 代码生成、内容优化 |

---

## 代码架构

### LLM客户端 (llm_client.py)

统一的LLM调用接口，支持流式响应。

```python
from llm_client import HelloAgentsLLM

llm = HelloAgentsLLM()
response = llm.think(messages)
```

### 工具系统 (tools.py)

工具定义和执行的管理器。

```python
from tools import ToolExecutor, search

executor = ToolExecutor()
executor.registerTool("Search", "搜索工具描述", search)
result = executor.getTool("Search")("查询内容")
```

### 记忆模块 (memory.py)

存储智能体的行动与反思轨迹。

```python
from memory import Memory

memory = Memory()
memory.add_record("execution", "代码内容")
trajectory = memory.get_trajectory()
```

---

## 学习要点

### ReAct范式
1. **思考-行动-观察循环**：每步都基于上一步的观察结果
2. **工具协同**：LLM推理 + 工具执行
3. **动态纠错**：根据反馈实时调整策略

### Plan-and-Solve范式
1. **两阶段解耦**：规划阶段 vs 执行阶段
2. **结构化分解**：复杂问题→步骤列表
3. **状态管理**：历史结果在步骤间传递

### Reflection范式
1. **迭代优化**：执行→反思→优化循环
2. **质量提升**：从功能正确到性能优化
3. **短期记忆**：存储完整迭代轨迹

---

## 扩展练习

1. 为ReAct智能体添加更多工具（计算器、天气查询等）
2. 实现动态重规划的Plan-and-Solve
3. 设计多维度Reflection机制
4. 组合三种范式构建混合智能体

---

## 参考资源

- [DataWhale Hello-Agents教程](https://github.com/datawhalechina/hello-agents)
- [ReAct论文](https://arxiv.org/abs/2210.03629)
- [Plan-and-Solve论文](https://arxiv.org/abs/2305.04091)
- [Reflexion论文](https://arxiv.org/abs/2303.11366)

---

## 许可证

MIT License

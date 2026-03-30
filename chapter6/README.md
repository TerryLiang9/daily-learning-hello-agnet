# 第六章：框架开发实践

> 学习AutoGen、AgentScope、LangGraph等主流框架

**本章重点**：
- 掌握主流Agent框架的使用
- LangGraph实战：状态图建模
- AutoGen多智能体协作
- AgentScope模块化开发

---

## 学习笔记

### 6.1 主流框架对比

| 框架 | 特点 | 优势 | 适用场景 |
|------|------|------|----------|
| **LangGraph** | 状态图建模 | 可视化、可控性强 | 复杂工作流、需要精确控制 |
| **AutoGen** | 多智能体对话 | 自动协商、角色分工 | 协作任务、团队模拟 |
| **AgentScope** | 模块化设计 | 易于扩展、跨语言 | 大型项目、企业应用 |

### 6.2 LangGraph实战

#### 核心概念

```
State（状态） → Node（节点） → Edge（边）
```

- **State**：在节点间传递的数据
- **Node**：处理状态的函数
- **Edge**：连接节点的路径

#### 状态图示例

```python
from typing import TypedDict, Annotated, Sequence
import operator
from langgraph.graph import StateGraph, END

# 定义状态
class AgentState(TypedDict):
    messages: Annotated[Sequence[str], operator.add]
    current_step: str

# 定义节点
def research_node(state: AgentState):
    # 研究节点逻辑
    return {"messages": ["研究完成"]}

def write_node(state: AgentState):
    # 写作节点逻辑
    return {"messages": ["写作完成"]}

# 构建图
workflow = StateGraph(AgentState)
workflow.add_node("research", research_node)
workflow.add_node("write", write_node)
workflow.add_edge("research", "write")
workflow.add_edge("write", END)
```

---

## 实践项目

### 项目1：智能研究助手

使用LangGraph构建一个多步骤研究助手：

```python
# langgraph_researcher.py

from typing import TypedDict, Annotated, Sequence
import operator
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI

class ResearchState(TypedDict):
    """研究状态"""
    topic: str
    research_data: str
    draft: str
    final_report: str

class ResearchAgent:
    """基于LangGraph的研究助手"""

    def __init__(self, api_key: str):
        self.llm = ChatOpenAI(api_key=api_key)
        self.workflow = self._build_workflow()

    def _build_workflow(self):
        """构建研究工作流"""
        workflow = StateGraph(ResearchState)

        # 添加节点
        workflow.add_node("research", self.research_node)
        workflow.add_node("draft", self.draft_node)
        workflow.add_node("review", self.review_node)
        workflow.add_node("finalize", self.finalize_node)

        # 设置入口
        workflow.set_entry_point("research")

        # 添加边
        workflow.add_edge("research", "draft")
        workflow.add_edge("draft", "review")
        workflow.add_conditional_edges(
            "review",
            self.should_revise,
            {
                "revise": "draft",
                "finalize": "finalize"
            }
        )
        workflow.add_edge("finalize", END)

        return workflow.compile()

    def research_node(self, state: ResearchState):
        """研究节点：收集信息"""
        prompt = f"研究关于 {state['topic']} 的最新信息"
        # 调用LLM进行研究
        research_data = self._call_llm(prompt)
        return {"research_data": research_data}

    def draft_node(self, state: ResearchState):
        """起草节点：撰写初稿"""
        prompt = f"基于以下研究数据撰写报告初稿：\n{state['research_data']}"
        draft = self._call_llm(prompt)
        return {"draft": draft}

    def review_node(self, state: ResearchState):
        """评审节点：评估质量"""
        prompt = f"评审以下报告草稿：\n{state['draft']}\n\n是否需要修改？"
        review = self._call_llm(prompt)
        return {"review": review}

    def finalize_node(self, state: ResearchState):
        """最终化节点：生成最终报告"""
        final_report = state['draft']
        return {"final_report": final_report}

    def should_revise(self, state: ResearchState) -> str:
        """决策是否需要修改"""
        # 根据评审结果决定
        return "finalize" if "满意" in state.get('review', '') else "revise"

    def _call_llm(self, prompt: str) -> str:
        """调用LLM"""
        response = self.llm.invoke(prompt)
        return response.content

    def run(self, topic: str) -> str:
        """运行研究助手"""
        initial_state = {"topic": topic}
        result = self.workflow.invoke(initial_state)
        return result['final_report']


# 使用示例
if __name__ == "__main__":
    import os

    agent = ResearchAgent(api_key=os.getenv("OPENAI_API_KEY"))
    report = agent.run("人工智能在医疗领域的应用")
    print(report)
```

### 项目2：AutoGen多智能体系统

```python
# autogen_multi_agent.py

import autogen

config_list = [
    {
        "model": "gpt-4",
        "api_key": "YOUR_API_KEY"
    }
]

# 定义智能体
assistant = autogen.AssistantAgent(
    name="assistant",
    llm_config={
        "config_list": config_list,
        "temperature": 0
    }
)

user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=10,
    code_execution_config={
        "work_dir": "coding",
        "use_docker": False
    }
)

# 开始对话
user_proxy.initiate_chat(
    assistant,
    message="如何使用Python实现快速排序？"
)
```

---

## 实践练习

### 练习1：LangGraph状态图
1. 安装LangGraph：`pip install langgraph`
2. 实现一个包含3个节点的状态图
3. 添加条件边实现分支逻辑
4. 可视化状态图

### 练习2：AutoGen协作
1. 安装AutoGen：`pip install pyautogen`
2. 创建2个具有不同角色的智能体
3. 实现智能体间的对话协商
4. 记录并分析对话过程

---

## 学习总结

### 核心收获

1. **框架选择**：
   - 简单项目 → 手写代码
   - 中等复杂度 → LangGraph
   - 多智能体协作 → AutoGen
   - 企业级应用 → AgentScope

2. **设计模式**：
   - 状态图模式（LangGraph）
   - 对话模式（AutoGen）
   - 模块化模式（AgentScope）

3. **最佳实践**：
   - 明确定义状态结构
   - 合理划分节点职责
   - 添加错误处理
   - 实现日志记录

### 下一步学习

- 第七章：从零构建Agent框架
- 第八章：记忆与检索系统
- 第九章：上下文工程

---

## 参考资源

- [LangGraph文档](https://python.langchain.com/docs/langgraph)
- [AutoGen文档](https://microsoft.github.io/autogen/)
- [AgentScope文档](https://github.com/modelscope/agentscope)

---

## 许可证

MIT License

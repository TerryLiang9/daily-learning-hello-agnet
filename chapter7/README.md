# 第七章：构建你的Agent框架

> 从零开始构建一个轻量级智能体框架

**本章目标**：
- 理解Agent框架的核心架构
- 实现一个可扩展的框架
- 掌握框架设计原则

---

## 框架设计

### 核心组件

```
AgentFramework
├── Agent (智能体基类)
├── Memory (记忆模块)
├── Tools (工具系统)
├── Planner (规划器)
├── Executor (执行器)
└── Communication (通信模块)
```

---

## 实现代码

### 1. 框架核心

```python
# simple_agent_framework/core/agent.py

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class BaseAgent(ABC):
    """智能体基类"""

    def __init__(self, name: str, config: Optional[Dict] = None):
        self.name = name
        self.config = config or {}
        self.memory = []
        self.tools = {}

    @abstractmethod
    def think(self, input_data: Any) -> Any:
        """思考：处理输入并生成决策"""
        pass

    @abstractmethod
    def act(self, action: Any) -> Any:
        """行动：执行决策"""
        pass

    def remember(self, experience: Dict):
        """记住经验"""
        self.memory.append(experience)

    def recall(self, query: str) -> List[Dict]:
        """回忆相关经验"""
        # 简单实现：返回所有记忆
        return self.memory

    def register_tool(self, name: str, tool: callable):
        """注册工具"""
        self.tools[name] = tool

    def use_tool(self, name: str, *args, **kwargs) -> Any:
        """使用工具"""
        if name in self.tools:
            return self.tools[name](*args, **kwargs)
        raise ValueError(f"Tool {name} not found")


class ReActAgent(BaseAgent):
    """ReAct智能体实现"""

    def __init__(self, name: str, llm_client, config: Optional[Dict] = None):
        super().__init__(name, config)
        self.llm_client = llm_client
        self.max_steps = config.get("max_steps", 5)

    def think(self, input_data: str) -> Dict[str, str]:
        """思考：生成thought和action"""
        prompt = self._build_prompt(input_data)

        response = self.llm_client.think([{"role": "user", "content": prompt}])

        # 解析响应
        thought, action = self._parse_response(response)
        return {"thought": thought, "action": action}

    def act(self, action_dict: Dict) -> str:
        """行动：执行action并返回observation"""
        action = action_dict.get("action", "")

        if action.startswith("Finish"):
            return action  # 最终答案

        # 解析工具调用
        tool_name, tool_input = self._parse_action(action)
        observation = self.use_tool(tool_name, tool_input)
        return observation

    def run(self, question: str) -> str:
        """运行ReAct循环"""
        history = []

        for step in range(self.max_steps):
            # 1. 思考
            thought_action = self.think(question)

            # 2. 行动
            observation = self.act(thought_action)

            # 3. 记录
            history.append({
                "step": step + 1,
                "thought": thought_action["thought"],
                "action": thought_action["action"],
                "observation": observation
            })

            # 4. 检查是否完成
            if observation.startswith("Finish"):
                return observation

            # 5. 更新上下文
            question = self._update_context(question, thought_action, observation)

        return "未能在限定步数内完成任务"

    def _build_prompt(self, question: str) -> str:
        """构建提示词"""
        tools_desc = "\n".join([f"- {name}" for name in self.tools.keys()])
        return f"""
可用工具:
{tools_desc}

问题: {question}

请按以下格式回应:
Thought: [你的思考]
Action: [工具名[输入]] 或 Finish[答案]
"""

    def _parse_response(self, response: str) -> tuple:
        """解析LLM响应"""
        # 简化实现
        lines = response.split("\n")
        thought = ""
        action = ""

        for line in lines:
            if line.startswith("Thought:"):
                thought = line.replace("Thought:", "").strip()
            elif line.startswith("Action:"):
                action = line.replace("Action:", "").strip()

        return thought, action

    def _parse_action(self, action: str) -> tuple:
        """解析action字符串"""
        # 简化实现：Tool[input]
        import re
        match = re.match(r"(\w+)\[(.*)\]", action)
        if match:
            return match.group(1), match.group(2)
        return None, None

    def _update_context(self, question: str, thought_action: Dict, observation: str) -> str:
        """更新上下文"""
        return f"{question}\nThought: {thought_action['thought']}\nAction: {thought_action['action']}\nObservation: {observation}"
```

### 2. 记忆模块

```python
# simple_agent_framework/core/memory.py

from typing import Any, Dict, List, Optional
import json
from datetime import datetime


class Memory:
    """记忆模块"""

    def __init__(self, max_size: int = 1000):
        self.memories = []
        self.max_size = max_size

    def add(self, memory: Dict):
        """添加记忆"""
        memory["timestamp"] = datetime.now().isoformat()
        self.memories.append(memory)

        # 限制记忆大小
        if len(self.memories) > self.max_size:
            self.memories = self.memories[-self.max_size:]

    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        """搜索记忆"""
        # 简化实现：基于关键词搜索
        results = []
        for memory in self.memories:
            if query.lower() in str(memory).lower():
                results.append(memory)
                if len(results) >= top_k:
                    break
        return results

    def get_recent(self, n: int = 10) -> List[Dict]:
        """获取最近记忆"""
        return self.memories[-n:]

    def save(self, filepath: str):
        """保存记忆到文件"""
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(self.memories, f, ensure_ascii=False, indent=2)

    def load(self, filepath: str):
        """从文件加载记忆"""
        with open(filepath, "r", encoding="utf-8") as f:
            self.memories = json.load(f)


class WorkingMemory(Memory):
    """工作记忆：短期记忆"""

    def __init__(self, capacity: int = 7):
        super().__init__(max_size=capacity)

    def add(self, memory: Dict):
        """添加记忆，超出容量时移除最旧的"""
        super().add(memory)
        if len(self.memories) > self.max_size:
            self.memories.pop(0)


class LongTermMemory(Memory):
    """长期记忆：持久化存储"""

    def __init__(self, filepath: str):
        super().__init__(max_size=10000)
        self.filepath = filepath
        self.load(filepath)

    def add(self, memory: Dict):
        """添加记忆并保存"""
        super().add(memory)
        self.save(self.filepath)
```

### 3. 工具系统

```python
# simple_agent_framework/core/tools.py

from typing import Any, Callable, Dict, List


class Tool:
    """工具基类"""

    def __init__(self, name: str, description: str, func: Callable):
        self.name = name
        self.description = description
        self.func = func

    def __call__(self, *args, **kwargs) -> Any:
        """调用工具"""
        return self.func(*args, **kwargs)


class ToolRegistry:
    """工具注册表"""

    def __init__(self):
        self.tools: Dict[str, Tool] = {}

    def register(self, tool: Tool):
        """注册工具"""
        self.tools[tool.name] = tool

    def get(self, name: str) -> Optional[Tool]:
        """获取工具"""
        return self.tools.get(name)

    def list_tools(self) -> List[str]:
        """列出所有工具"""
        return list(self.tools.keys())

    def get_description(self, name: str) -> str:
        """获取工具描述"""
        tool = self.get(name)
        return tool.description if tool else ""


# 预定义工具
def search_tool(query: str) -> str:
    """搜索工具示例"""
    # 实际实现可以接入真实搜索API
    return f"搜索结果：关于 '{query}' 的信息"


def calculator_tool(expression: str) -> str:
    """计算器工具"""
    try:
        result = eval(expression)
        return f"计算结果：{result}"
    except Exception as e:
        return f"计算错误：{e}"


# 创建默认工具注册表
default_registry = ToolRegistry()
default_registry.register(Tool("search", "搜索信息", search_tool))
default_registry.register(Tool("calculator", "数学计算", calculator_tool))
```

### 4. 框架入口

```python
# simple_agent_framework/__init__.py

from .core.agent import BaseAgent, ReActAgent
from .core.memory import Memory, WorkingMemory, LongTermMemory
from .core.tools import Tool, ToolRegistry, default_registry

__version__ = "0.1.0"

__all__ = [
    "BaseAgent",
    "ReActAgent",
    "Memory",
    "WorkingMemory",
    "LongTermMemory",
    "Tool",
    "ToolRegistry",
    "default_registry",
]
```

---

## 使用示例

```python
# example.py

from simple_agent_framework import ReActAgent, default_registry
from llm_client import HelloAgentsLLM

# 初始化LLM客户端
llm = HelloAgentsLLM()

# 创建智能体
agent = ReActAgent(
    name="research_assistant",
    llm_client=llm,
    config={"max_steps": 5}
)

# 注册工具
for tool_name in default_registry.list_tools():
    tool = default_registry.get(tool_name)
    agent.register_tool(tool_name, tool.func)

# 运行
question = "计算 (123 + 456) * 789 / 12 的结果"
answer = agent.run(question)
print(answer)
```

---

## 学习总结

### 设计原则

1. **模块化**：各组件独立，易于替换
2. **可扩展**：支持自定义工具和智能体
3. **简单性**：核心逻辑清晰易懂
4. **实用性**：解决实际问题

### 架构优势

- 清晰的职责划分
- 灵活的组件组合
- 易于测试和调试
- 便于学习和扩展

---

## 许可证

MIT License

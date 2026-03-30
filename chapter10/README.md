# 第十章：智能体通信协议

> MCP、A2A、ANP等智能体间通信标准

**本章重点**：
- 理解智能体通信的必要性
- 学习主流通信协议
- 实现多智能体协作系统

---

## 学习笔记

### 10.1 为什么需要通信协议？

**智能体通信的核心价值**：

1. **任务分工**：不同智能体各司其职
2. **知识共享**：交换信息和经验
3. **协同决策**：通过协商达成共识
4. **系统扩展**：构建大规模智能体网络

### 10.2 主流通信协议

```
智能体通信协议
├── MCP (Model Context Protocol)
├── A2A (Agent-to-Agent)
├── ANP (Agent Network Protocol)
└── 自定义协议
```

| 协议 | 特点 | 应用场景 |
|------|------|----------|
| **MCP** | 标准化、易集成 | LLM应用、工具调用 |
| **A2A** | 点对点、灵活 | 简单多智能体系统 |
| **ANP** | 网络化、可扩展 | 复杂智能体网络 |

---

## 实现代码

### 1. 简单的A2A通信协议

```python
# a2a_protocol.py

from typing import Dict, List, Any, Optional
from enum import Enum
import json
from datetime import datetime


class MessageType(Enum):
    """消息类型"""
    REQUEST = "request"
    RESPONSE = "response"
    NOTIFICATION = "notification"
    BROADCAST = "broadcast"


class Message:
    """智能体间消息"""

    def __init__(self,
                 sender: str,
                 receiver: str,
                 message_type: MessageType,
                 content: Any,
                 message_id: Optional[str] = None):
        self.sender = sender
        self.receiver = receiver
        self.message_type = message_type
        self.content = content
        self.message_id = message_id or self._generate_id()
        self.timestamp = datetime.now().isoformat()

    def _generate_id(self) -> str:
        """生成消息ID"""
        import uuid
        return str(uuid.uuid4())

    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "message_id": self.message_id,
            "sender": self.sender,
            "receiver": self.receiver,
            "type": self.message_type.value,
            "content": self.content,
            "timestamp": self.timestamp
        }

    def to_json(self) -> str:
        """转换为JSON"""
        return json.dumps(self.to_dict(), ensure_ascii=False)

    @classmethod
    def from_json(cls, json_str: str) -> 'Message':
        """从JSON创建消息"""
        data = json.loads(json_str)
        return cls(
            sender=data["sender"],
            receiver=data["receiver"],
            message_type=MessageType(data["type"]),
            content=data["content"],
            message_id=data["message_id"]
        )


class MessageQueue:
    """消息队列"""

    def __init__(self):
        self.queues: Dict[str, List[Message]] = {}

    def send(self, message: Message):
        """发送消息"""
        receiver = message.receiver

        if receiver not in self.queues:
            self.queues[receiver] = []

        self.queues[receiver].append(message)

    def receive(self, agent_id: str) -> Optional[Message]:
        """接收消息"""
        if agent_id in self.queues and self.queues[agent_id]:
            return self.queues[agent_id].pop(0)
        return None

    def peek(self, agent_id: str) -> int:
        """查看待处理消息数量"""
        if agent_id in self.queues:
            return len(self.queues[agent_id])
        return 0


class Agent:
    """智能体基类"""

    def __init__(self, name: str, message_queue: MessageQueue):
        self.name = name
        self.message_queue = message_queue
        self.running = False

    def start(self):
        """启动智能体"""
        self.running = True
        print(f"[{self.name}] 智能体已启动")

    def stop(self):
        """停止智能体"""
        self.running = False
        print(f"[{self.name}] 智能体已停止")

    def send_message(self, receiver: str, content: Any, message_type: MessageType = MessageType.REQUEST):
        """发送消息"""
        message = Message(
            sender=self.name,
            receiver=receiver,
            message_type=message_type,
            content=content
        )
        self.message_queue.send(message)
        print(f"[{self.name}] 发送消息到 {receiver}: {content}")

    def receive_message(self) -> Optional[Message]:
        """接收消息"""
        return self.message_queue.receive(self.name)

    def process_message(self, message: Message):
        """处理消息（子类实现）"""
        raise NotImplementedError

    def run(self):
        """运行智能体主循环"""
        while self.running:
            message = self.receive_message()
            if message:
                self.process_message(message)
```

### 2. 多智能体协作系统

```python
# multi_agent_system.py

from a2a_protocol import Agent, Message, MessageType, MessageQueue


class ResearchAgent(Agent):
    """研究智能体"""

    def __init__(self, name: str, message_queue: MessageQueue):
        super().__init__(name, message_queue)
        self.knowledge_base = {
            "AI": "人工智能是计算机科学的一个分支",
            "ML": "机器学习是AI的子领域",
            "DL": "深度学习使用神经网络"
        }

    def process_message(self, message: Message):
        """处理查询消息"""
        query = message.content

        # 查找知识库
        answer = self.knowledge_base.get(query, "抱歉，我不了解这个话题")

        # 发送回复
        self.send_message(
            receiver=message.sender,
            content=answer,
            message_type=MessageType.RESPONSE
        )


class WriterAgent(Agent):
    """写作智能体"""

    def __init__(self, name: str, message_queue: MessageQueue):
        super().__init__(name, message_queue)
        self.drafts = []

    def process_message(self, message: Message):
        """处理写作请求"""
        topic = message.content

        # 生成草稿
        draft = f"关于{topic}的文章草稿..."
        self.drafts.append(draft)

        # 发送回复
        self.send_message(
            receiver=message.sender,
            content=f"已完成{topic}的草稿",
            message_type=MessageType.RESPONSE
        )


class CoordinatorAgent(Agent):
    """协调者智能体"""

    def __init__(self, name: str, message_queue: MessageQueue):
        super().__init__(name, message_queue)
        self.agents = []

    def register_agent(self, agent: Agent):
        """注册智能体"""
        self.agents.append(agent)

    def delegate_task(self, task: str, agent_name: str):
        """委派任务"""
        print(f"[{self.name}] 委派任务 '{task}' 给 {agent_name}")
        self.send_message(agent_name, task)

    def process_message(self, message: Message):
        """处理响应"""
        if message.message_type == MessageType.RESPONSE:
            print(f"[{self.name}] 收到 {message.sender} 的回复: {message.content}")


# 使用示例
if __name__ == "__main__":
    # 创建消息队列
    message_queue = MessageQueue()

    # 创建智能体
    coordinator = CoordinatorAgent("协调者", message_queue)
    researcher = ResearchAgent("研究者", message_queue)
    writer = WriterAgent("写作者", message_queue)

    # 注册智能体
    coordinator.register_agent(researcher)
    coordinator.register_agent(writer)

    # 启动所有智能体
    coordinator.start()
    researcher.start()
    writer.start()

    # 模拟任务委派
    coordinator.delegate_task("AI", "研究者")
    coordinator.delegate_task("AI", "写作者")

    # 处理消息（简化实现）
    for _ in range(3):
        for agent in [coordinator, researcher, writer]:
            msg = agent.receive_message()
            if msg:
                agent.process_message(msg)

    # 停止所有智能体
    coordinator.stop()
    researcher.stop()
    writer.stop()
```

### 3. MCP风格通信实现

```python
# mcp_style_protocol.py

from typing import Dict, List, Callable, Any


class MCPServer:
    """MCP风格服务器"""

    def __init__(self, name: str):
        self.name = name
        self.tools: Dict[str, Callable] = {}
        self.resources: Dict[str, Any] = {}

    def register_tool(self, name: str, func: Callable):
        """注册工具"""
        self.tools[name] = func
        print(f"[{self.name}] 注册工具: {name}")

    def register_resource(self, name: str, resource: Any):
        """注册资源"""
        self.resources[name] = resource
        print(f"[{self.name}] 注册资源: {name}")

    def call_tool(self, tool_name: str, *args, **kwargs) -> Any:
        """调用工具"""
        if tool_name in self.tools:
            return self.tools[tool_name](*args, **kwargs)
        raise ValueError(f"工具 {tool_name} 不存在")

    def get_resource(self, resource_name: str) -> Any:
        """获取资源"""
        if resource_name in self.resources:
            return self.resources[resource_name]
        raise ValueError(f"资源 {resource_name} 不存在")


class MCPClient:
    """MCP风格客户端"""

    def __init__(self, name: str, server: MCPServer):
        self.name = name
        self.server = server

    def use_tool(self, tool_name: str, *args, **kwargs) -> Any:
        """使用服务器的工具"""
        print(f"[{self.name}] 调用工具: {tool_name}")
        return self.server.call_tool(tool_name, *args, **kwargs)

    def access_resource(self, resource_name: str) -> Any:
        """访问服务器的资源"""
        print(f"[{self.name}] 访问资源: {resource_name}")
        return self.server.get_resource(resource_name)


# 使用示例
if __name__ == "__main__":
    # 创建服务器
    server = MCPServer("数据服务器")

    # 注册工具
    def calculate(expression: str) -> float:
        return eval(expression)

    def search_database(query: str) -> str:
        return f"查询结果: {query}"

    server.register_tool("calculator", calculate)
    server.register_tool("search", search_database)

    # 注册资源
    server.register_resource("knowledge_base", {
        "AI": "人工智能",
        "ML": "机器学习"
    })

    # 创建客户端
    client1 = MCPClient("客户端1", server)
    client2 = MCPClient("客户端2", server)

    # 使用工具和资源
    result1 = client1.use_tool("calculator", "2 + 3")
    print(f"结果: {result1}")

    result2 = client2.use_tool("search", "深度学习")
    print(f"结果: {result2}")

    knowledge = client1.access_resource("knowledge_base")
    print(f"知识库: {knowledge}")
```

---

## 实践项目

### 项目：智能团队协作系统

**目标**：构建一个模拟团队协作的多智能体系统

```python
# team_collaboration.py

from a2a_protocol import Agent, Message, MessageType, MessageQueue


class TeamMember(Agent):
    """团队成员"""

    def __init__(self, name: str, role: str, message_queue: MessageQueue):
        super().__init__(name, message_queue)
        self.role = role
        self.skills = []

    def add_skill(self, skill: str):
        """添加技能"""
        self.skills.append(skill)

    def can_handle(self, task: str) -> bool:
        """判断是否能处理任务"""
        return any(skill in task for skill in self.skills)

    def process_message(self, message: Message):
        """处理任务消息"""
        task = message.content

        print(f"[{self.name}] ({self.role}) 正在处理任务: {task}")

        # 模拟任务处理
        result = f"{self.name} 已完成 {task}"

        # 发送完成通知
        self.send_message(
            receiver=message.sender,
            content=result,
            message_type=MessageType.RESPONSE
        )


class ProjectManager(Agent):
    """项目经理"""

    def __init__(self, name: str, message_queue: MessageQueue):
        super().__init__(name, message_queue)
        self.team = []
        self.task_queue = []

    def add_team_member(self, member: TeamMember):
        """添加团队成员"""
        self.team.append(member)
        print(f"[{self.name}] 添加团队成员: {member.name} ({member.role})")

    def assign_task(self, task: str):
        """分配任务"""
        # 找到合适的成员
        for member in self.team:
            if member.can_handle(task):
                print(f"[{self.name}] 将任务 '{task}' 分配给 {member.name}")
                self.send_message(member.name, task)
                return

        # 没找到合适的成员
        print(f"[{self.name}] 警告: 没有成员能处理任务 '{task}'")

    def process_message(self, message: Message):
        """处理任务完成通知"""
        if message.message_type == MessageType.RESPONSE:
            print(f"[{self.name}] 收到完成通知: {message.content}")


# 使用示例
if __name__ == "__main__":
    # 创建消息队列
    message_queue = MessageQueue()

    # 创建团队
    manager = ProjectManager("项目经理", message_queue)

    developer = TeamMember("张三", "开发者", message_queue)
    developer.add_skill("编程")
    developer.add_skill("调试")

    designer = TeamMember("李四", "设计师", message_queue)
    designer.add_skill("设计")
    designer.add_skill("UI")

    tester = TeamMember("王五", "测试员", message_queue)
    tester.add_skill("测试")
    tester.add_skill("质量保证")

    # 组建团队
    manager.add_team_member(developer)
    manager.add_team_member(designer)
    manager.add_team_member(tester)

    # 启动所有成员
    for agent in [manager, developer, designer, tester]:
        agent.start()

    # 分配任务
    tasks = [
        "编写用户登录功能",
        "设计主界面UI",
        "测试购物车功能",
        "修复登录bug"
    ]

    for task in tasks:
        manager.assign_task(task)

    # 处理消息
    for _ in range(len(tasks) + 2):
        for agent in [manager, developer, designer, tester]:
            msg = agent.receive_message()
            if msg:
                agent.process_message(msg)

    # 停止所有成员
    for agent in [manager, developer, designer, tester]:
        agent.stop()
```

---

## 学习总结

### 核心概念

1. **消息传递**：智能体间的基本通信方式
2. **协议标准化**：统一的通信格式
3. **异步处理**：非阻塞的消息处理
4. **任务协调**：智能体间的任务分配

### 协议选择

- **简单系统**：A2A协议
- **标准化需求**：MCP协议
- **大规模网络**：ANP协议

---

## 参考资源

- [MCP协议规范](https://modelcontextprotocol.io/)
- [Multi-Agent系统论文](https://arxiv.org/abs/2306.05685)
- [LangChain Multi-Agent](https://python.langchain.com/docs/use_cases/agent_simulations)

---

## 许可证

MIT License

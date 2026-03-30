# 第九章：上下文工程

> 掌握持续交互中的情境理解技术

**本章重点**：
- 理解上下文在对话中的重要性
- 上下文压缩与选择策略
- 实现高效的多轮对话系统

---

## 学习笔记

### 9.1 上下文的重要性

**为什么需要上下文工程？**

1. **LLM的上下文窗口限制**：模型有最大token限制
2. **信息过载**：过多历史信息会干扰模型
3. **成本优化**：减少不必要的token消耗
4. **性能提升**：精准的相关信息提升回答质量

### 9.2 上下文管理策略

```
上下文管理策略
├── 滑动窗口（Sliding Window）
├── 摘要压缩（Summarization）
├── 关键信息提取（Key Extraction）
├── 分层存储（Hierarchical Memory）
└── 智能检索（Retrieval-based）
```

| 策略 | 原理 | 优势 | 适用场景 |
|------|------|------|----------|
| 滑动窗口 | 保留最近N轮对话 | 简单高效 | 短期对话 |
| 摘要压缩 | 定期总结历史信息 | 节省token | 长对话 |
| 关键信息提取 | 只保留重要信息 | 精准聚焦 | 任务型对话 |
| 分层存储 | 短期+长期记忆 | 模拟人类记忆 | 复杂应用 |
| 智能检索 | 按需检索相关上下文 | 高效精准 | 大规模对话 |

---

## 实现代码

### 1. 上下文管理器

```python
# context_manager.py

from typing import List, Dict, Optional
from datetime import datetime


class ContextManager:
    """上下文管理器"""

    def __init__(self,
                 max_history: int = 10,
                 summary_threshold: int = 20,
                 use_compression: bool = True):
        self.max_history = max_history
        self.summary_threshold = summary_threshold
        self.use_compression = use_compression

        self.conversation_history = []
        self.summaries = []

    def add_message(self, role: str, content: str):
        """添加消息"""
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        }
        self.conversation_history.append(message)

        # 检查是否需要压缩
        if self.use_compression and len(self.conversation_history) > self.summary_threshold:
            self._compress_history()

    def _compress_history(self):
        """压缩历史对话"""
        # 保留最近的消息
        recent_messages = self.conversation_history[-self.max_history:]

        # 早期消息进行摘要
        old_messages = self.conversation_history[:-self.max_history]
        if old_messages:
            summary = self._create_summary(old_messages)
            self.summaries.append(summary)

        # 更新历史
        self.conversation_history = recent_messages

    def _create_summary(self, messages: List[Dict]) -> str:
        """创建对话摘要"""
        # 简单实现：提取关键信息
        # 实际应用中可以使用LLM生成摘要
        key_points = []

        for msg in messages:
            if msg["role"] == "user":
                # 提取用户的问题
                key_points.append(f"用户询问: {msg['content'][:50]}...")

        return " | ".join(key_points)

    def get_context(self) -> str:
        """获取用于LLM的上下文"""
        context_parts = []

        # 添加历史摘要
        if self.summaries:
            context_parts.append("[历史对话摘要]")
            context_parts.append("\n".join(self.summaries))

        # 添加最近对话
        if self.conversation_history:
            context_parts.append("[最近对话]")
            for msg in self.conversation_history:
                role_name = "用户" if msg["role"] == "user" else "助手"
                context_parts.append(f"{role_name}: {msg['content']}")

        return "\n\n".join(context_parts)

    def clear(self):
        """清空上下文"""
        self.conversation_history = []
        self.summaries = []


class SlidingWindowContext(ContextManager):
    """滑动窗口上下文管理"""

    def add_message(self, role: str, content: str):
        """添加消息，超出限制时移除最旧的"""
        super().add_message(role, content)

        # 严格限制历史数量
        if len(self.conversation_history) > self.max_history:
            self.conversation_history = self.conversation_history[-self.max_history:]


class KeyExtractionContext(ContextManager):
    """关键信息提取上下文管理"""

    def __init__(self, max_history: int = 10):
        super().__init__(max_history)
        self.key_information = {}

    def add_message(self, role: str, content: str):
        """添加消息并提取关键信息"""
        super().add_message(role, content)

        # 提取关键信息
        if role == "user":
            self._extract_key_info(content)

    def _extract_key_info(self, content: str):
        """提取关键信息（简化实现）"""
        # 实际应用中可以使用NLP技术或LLM
        keywords = ["姓名", "年龄", "喜欢", "想要", "需要"]

        for keyword in keywords:
            if keyword in content:
                # 简单提取，实际应该更复杂
                start_idx = content.find(keyword)
                end_idx = start_idx + 50
                if end_idx > len(content):
                    end_idx = len(content)
                self.key_information[keyword] = content[start_idx:end_idx]

    def get_context(self) -> str:
        """获取包含关键信息的上下文"""
        context_parts = []

        # 添加关键信息
        if self.key_information:
            context_parts.append("[关键信息]")
            for key, value in self.key_information.items():
                context_parts.append(f"{key}: {value}")

        # 添加最近对话
        if self.conversation_history:
            context_parts.append("[最近对话]")
            for msg in self.conversation_history[-5:]:  # 只保留最近5条
                role_name = "用户" if msg["role"] == "user" else "助手"
                context_parts.append(f"{role_name}: {msg['content']}")

        return "\n\n".join(context_parts)
```

### 2. 智能对话系统

```python
# smart_conversation.py

from context_manager import ContextManager, KeyExtractionContext
from llm_client import HelloAgentsLLM


class SmartConversationSystem:
    """智能对话系统"""

    def __init__(self,
                 llm_client: HelloAgentsLLM,
                 context_manager: Optional[ContextManager] = None):
        self.llm_client = llm_client
        self.context_manager = context_manager or ContextManager()

    def chat(self, user_input: str) -> str:
        """与用户对话"""
        # 1. 添加用户消息到上下文
        self.context_manager.add_message("user", user_input)

        # 2. 获取上下文
        context = self.context_manager.get_context()

        # 3. 构建提示词
        prompt = f"""
你是一个智能助手。请基于以下上下文信息回答用户的问题。

{context}

当前用户问题：{user_input}

请给出你的回答：
"""

        # 4. 调用LLM
        messages = [{"role": "user", "content": prompt}]
        response = self.llm_client.think(messages)

        # 5. 添加助手回复到上下文
        self.context_manager.add_message("assistant", response)

        return response

    def reset(self):
        """重置对话"""
        self.context_manager.clear()


# 使用示例
if __name__ == "__main__":
    import os

    # 初始化
    llm = HelloAgentsLLM()
    context_mgr = KeyExtractionContext(max_history=10)
    chat_system = SmartConversationSystem(llm, context_mgr)

    # 模拟对话
    conversations = [
        "我叫张三，今年25岁",
        "我喜欢编程和AI",
        "你还记得我的名字吗？",
        "我今年多大了？",
        "给我推荐一些学习AI的资源"
    ]

    for user_msg in conversations:
        print(f"\n用户: {user_msg}")
        response = chat_system.chat(user_msg)
        print(f"助手: {response}")
```

---

## 实践项目

### 项目：个性化客服助手

**目标**：构建一个能记住用户偏好和历史的高质量客服系统

```python
# customer_service_agent.py

from smart_conversation import SmartConversationSystem
from context_manager import KeyExtractionContext
from llm_client import HelloAgentsLLM


class CustomerServiceAgent:
    """个性化客服助手"""

    def __init__(self, llm_client):
        self.llm_client = llm_client
        self.context_manager = KeyExtractionContext(max_history=15)
        self.conversation_system = SmartConversationSystem(llm_client, self.context_manager)

        # 用户档案
        self.user_profile = {
            "name": None,
            "preferences": [],
            "history": []
        }

    def handle_query(self, user_input: str) -> str:
        """处理用户查询"""
        # 1. 提取用户意图
        intent = self._classify_intent(user_input)

        # 2. 根据意图处理
        if intent == "complaint":
            return self._handle_complaint(user_input)
        elif intent == "inquiry":
            return self._handle_inquiry(user_input)
        elif intent == "preference":
            return self._update_preferences(user_input)
        else:
            # 使用智能对话系统
            return self.conversation_system.chat(user_input)

    def _classify_intent(self, text: str) -> str:
        """分类用户意图"""
        # 简化实现
        if any(word in text for word in ["投诉", "不满", "问题"]):
            return "complaint"
        elif any(word in text for word in ["喜欢", "偏好", "兴趣"]):
            return "preference"
        else:
            return "inquiry"

    def _handle_complaint(self, text: str) -> str:
        """处理投诉"""
        response = "抱歉给您带来不便。我们已记录您的问题，客服专员会尽快联系您。"
        self.conversation_system.context_manager.add_message("assistant", response)
        return response

    def _handle_inquiry(self, text: str) -> str:
        """处理咨询"""
        # 可以结合知识库检索
        return self.conversation_system.chat(text)

    def _update_preferences(self, text: str) -> str:
        """更新用户偏好"""
        # 提取偏好信息
        self.user_profile["preferences"].append(text)
        response = "感谢您的反馈，我们已记录您的偏好。"
        self.conversation_system.context_manager.add_message("assistant", response)
        return response


# 使用示例
if __name__ == "__main__":
    import os

    llm = HelloAgentsLLM()
    agent = CustomerServiceAgent(llm)

    # 模拟客服对话
    queries = [
        "我喜欢简洁的产品设计",
        "你们的产品有什么特色？",
        "我对最近的服务不太满意"
    ]

    for query in queries:
        print(f"\n客户: {query}")
        response = agent.handle_query(query)
        print(f"客服: {response}")
```

---

## 学习总结

### 核心概念

1. **上下文窗口管理**：处理token限制
2. **信息压缩**：保留关键信息
3. **智能检索**：按需获取相关内容
4. **分层记忆**：模拟人类记忆机制

### 最佳实践

1. 根据应用场景选择合适的上下文策略
2. 定期评估和优化上下文管理效果
3. 平衡信息完整性和成本效率
4. 结合检索增强生成（RAG）提升质量

---

## 参考资源

- [LangChain Memory文档](https://python.langchain.com/docs/modules/memory/)
- [上下文窗口优化](https://www.anthropic.com/index/context-window-management)
- [对话系统最佳实践](https://arxiv.org/abs/2306.05685)

---

## 许可证

MIT License

# 第十六章：毕业设计

> 构建属于你的完整多智能体应用

**本章目标**：
- 综合运用所学知识
- 独立完成一个完整项目
- 展示智能体开发能力

---

## 项目选题建议

### 选项1：智能学习助手

**功能**：
- 📚 个性化学习计划制定
- 💡 智能问答和知识点讲解
- 📝 作业批改和学习建议
- 📊 学习进度追踪

**技术栈**：
- LangChain框架
- RAG系统
- 多智能体协作

### 选项2：智能客服系统

**功能**：
- 💬 自然语言对话
- 🔍 知识库检索
- 🎯 意图识别
- 📈 情感分析

**技术栈**：
- 对话管理
- 知识图谱
- 情感计算

### 选项3：自动化研究助手

**功能**：
- 🔍 多源信息搜索
- 📊 数据分析和可视化
- 📝 报告自动生成
- 🔄 迭代优化

**技术栈**：
- 爬虫技术
- 数据分析
- 文档生成

---

## 完整示例：全能智能助手

让我为你展示一个完整的毕业设计项目框架。

### 项目架构

```
intelligent-assistant/
├── agents/                    # 智能体模块
│   ├── base_agent.py         # 基础智能体
│   ├── research_agent.py     # 研究智能体
│   ├── writing_agent.py      # 写作智能体
│   └── analysis_agent.py     # 分析智能体
├── tools/                     # 工具模块
│   ├── search.py             # 搜索工具
│   ├── calculator.py         # 计算工具
│   └── database.py           # 数据库工具
├── memory/                    # 记忆模块
│   ├── vector_store.py       # 向量存储
│   └── kg_store.py           # 知识图谱
├── ui/                        # 用户界面
│   ├── cli.py                # 命令行界面
│   └── web.py                # Web界面
├── evaluation/                # 评估模块
│   └── metrics.py            # 评估指标
├── config/                    # 配置文件
│   └── settings.py           # 系统配置
└── main.py                    # 主程序
```

### 核心代码

```python
# main.py

"""
全能智能助手 - 毕业设计项目
作者: [你的名字]
日期: 2026-03-30
"""

from agents.base_agent import BaseAgent
from agents.research_agent import ResearchAgent
from agents.writing_agent import WritingAgent
from agents.analysis_agent import AnalysisAgent
from tools.registry import ToolRegistry
from memory.long_term_memory import LongTermMemory
from ui.cli import CLIInterface
from config.settings import Settings
import logging


class IntelligentAssistant:
    """全能智能助手主类"""

    def __init__(self, config_path: str = "config/settings.json"):
        # 加载配置
        self.settings = Settings(config_path)

        # 初始化日志
        logging.basicConfig(
            level=self.settings.log_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

        # 初始化组件
        self.logger.info("初始化智能助手...")
        self.tool_registry = ToolRegistry()
        self.memory = LongTermMemory(self.settings.memory_path)

        # 初始化智能体
        self.agents = {
            "research": ResearchAgent(self.settings.llm_config, self.tool_registry),
            "writing": WritingAgent(self.settings.llm_config),
            "analysis": AnalysisAgent(self.settings.llm_config)
        }

        self.logger.info("智能助手初始化完成")

    def process_request(self, user_input: str) -> str:
        """处理用户请求"""
        self.logger.info(f"用户输入: {user_input}")

        # 1. 意图识别
        intent = self._classify_intent(user_input)

        # 2. 路由到相应智能体
        if intent == "research":
            response = self.agents["research"].handle(user_input)
        elif intent == "writing":
            response = self.agents["writing"].handle(user_input)
        elif intent == "analysis":
            response = self.agents["analysis"].handle(user_input)
        else:
            response = self._general_response(user_input)

        # 3. 存储到记忆
        self.memory.add({
            "user_input": user_input,
            "intent": intent,
            "response": response,
            "timestamp": datetime.now()
        })

        return response

    def _classify_intent(self, text: str) -> str:
        """分类用户意图"""
        # 简化实现
        keywords = {
            "research": ["搜索", "查找", "研究", "了解"],
            "writing": ["写", "生成", "创作", "撰写"],
            "analysis": ["分析", "统计", "计算", "评估"]
        }

        for intent, words in keywords.items():
            if any(word in text for word in words):
                return intent

        return "general"

    def _general_response(self, text: str) -> str:
        """通用回复"""
        return f"我收到了你的消息：{text}"

    def run(self):
        """运行智能助手"""
        interface = CLIInterface(self)
        interface.start()


def main():
    """主函数"""
    assistant = IntelligentAssistant()
    assistant.run()


if __name__ == "__main__":
    main()
```

### 基础智能体

```python
# agents/base_agent.py

from abc import ABC, abstractmethod
from typing import Dict, Any


class BaseAgent(ABC):
    """智能体基类"""

    def __init__(self, llm_config: Dict[str, Any]):
        self.llm_config = llm_config
        self.name = self.__class__.__name__
        self.memory = []

    @abstractmethod
    def handle(self, task: str) -> str:
        """处理任务"""
        pass

    def remember(self, experience: Dict):
        """记住经验"""
        self.memory.append(experience)

    def recall(self, query: str) -> list:
        """回忆相关经验"""
        # 简化实现
        return [m for m in self.memory if query.lower() in str(m).lower()]
```

### 研究智能体

```python
# agents/research_agent.py

from .base_agent import BaseAgent
from tools.search import SearchTool
from tools.registry import ToolRegistry
from llm_client import HelloAgentsLLM


class ResearchAgent(BaseAgent):
    """研究智能体"""

    def __init__(self, llm_config: Dict, tool_registry: ToolRegistry):
        super().__init__(llm_config)
        self.llm = HelloAgentsLLM()
        self.tool_registry = tool_registry

        # 注册工具
        self.search_tool = SearchTool()
        self.tool_registry.register("search", self.search_tool)

    def handle(self, task: str) -> str:
        """处理研究任务"""
        # 1. 提取关键词
        keywords = self._extract_keywords(task)

        # 2. 搜索信息
        results = self.search_tool.search(keywords)

        # 3. 分析总结
        summary = self._summarize_results(task, results)

        return summary

    def _extract_keywords(self, text: str) -> str:
        """提取关键词"""
        prompt = f"从以下文本中提取搜索关键词：{text}"
        response = self.llm.think([{"role": "user", "content": prompt}])
        return response

    def _summarize_results(self, task: str, results: list) -> str:
        """总结搜索结果"""
        results_text = "\n".join([r["snippet"] for r in results])

        prompt = f"""
基于以下搜索结果，回答问题：{task}

搜索结果：
{results_text}

请提供详细、准确的答案。
"""

        response = self.llm.think([{"role": "user", "content": prompt}])
        return response
```

### 工具注册表

```python
# tools/registry.py

from typing import Dict, Callable


class ToolRegistry:
    """工具注册表"""

    def __init__(self):
        self.tools: Dict[str, Callable] = {}

    def register(self, name: str, tool: Callable):
        """注册工具"""
        self.tools[name] = tool

    def get(self, name: str) -> Callable:
        """获取工具"""
        return self.tools.get(name)

    def list_tools(self) -> list:
        """列出所有工具"""
        return list(self.tools.keys())
```

### 命令行界面

```python
# ui/cli.py

from typing import Callable


class CLIInterface:
    """命令行界面"""

    def __init__(self, assistant: Callable):
        self.assistant = assistant

    def start(self):
        """启动交互界面"""
        print("\n" + "="*50)
        print("🤖 全能智能助手")
        print("="*50)
        print("\n输入 'quit' 或 'exit' 退出\n")

        while True:
            try:
                # 获取用户输入
                user_input = input("👤 你: ").strip()

                # 检查退出命令
                if user_input.lower() in ['quit', 'exit', '退出']:
                    print("\n👋 再见！")
                    break

                # 处理请求
                if not user_input:
                    continue

                response = self.assistant.process_request(user_input)

                # 显示回复
                print(f"\n🤖 助手: {response}\n")

            except KeyboardInterrupt:
                print("\n\n👋 再见！")
                break
            except Exception as e:
                print(f"\n❌ 错误: {e}\n")
```

---

## 项目文档

### README.md

```markdown
# 全能智能助手

一个基于多智能体架构的智能助手系统，集成研究、写作、分析等能力。

## 功能特性

- 🔍 智能搜索和研究
- ✍️ 内容创作和写作
- 📊 数据分析和可视化
- 💾 长期记忆管理
- 🎯 多智能体协作

## 安装

```bash
git clone https://github.com/yourusername/intelligent-assistant.git
cd intelligent-assistant
pip install -r requirements.txt
```

## 使用

```bash
python main.py
```

## 架构

```
用户输入 → 意图识别 → 智能体路由 → 工具调用 → 结果返回
```

## 贡献

欢迎提交Pull Request！
```

### API文档

```python
# docs/api.py

"""
API文档
"""

class IntelligentAssistant:
    """智能助手API"""

    def process_request(self, user_input: str) -> str:
        """
        处理用户请求

        参数:
            user_input: 用户输入文本

        返回:
            str: 助手回复
        """
        pass
```

---

## 评估和测试

### 单元测试

```python
# tests/test_assistant.py

import unittest
from main import IntelligentAssistant


class TestIntelligentAssistant(unittest.TestCase):
    """测试智能助手"""

    def setUp(self):
        """测试前准备"""
        self.assistant = IntelligentAssistant()

    def test_intent_classification(self):
        """测试意图分类"""
        intent1 = self.assistant._classify_intent("搜索Python教程")
        self.assertEqual(intent1, "research")

        intent2 = self.assistant._classify_intent("写一首诗")
        self.assertEqual(intent2, "writing")

    def test_research_capability(self):
        """测试研究能力"""
        response = self.assistant.process_request("研究人工智能")
        self.assertIsNotNone(response)
        self.assertGreater(len(response), 10)


if __name__ == "__main__":
    unittest.main()
```

### 性能评估

```python
# evaluation/performance.py

import time
from typing import List


class PerformanceEvaluator:
    """性能评估器"""

    def __init__(self, assistant):
        self.assistant = assistant

    def evaluate_response_time(self, test_inputs: List[str]) -> Dict:
        """评估响应时间"""
        times = []

        for test_input in test_inputs:
            start = time.time()
            self.assistant.process_request(test_input)
            end = time.time()

            times.append(end - start)

        return {
            "average_time": sum(times) / len(times),
            "max_time": max(times),
            "min_time": min(times)
        }

    def evaluate_accuracy(self, test_cases: List[Dict]) -> float:
        """评估准确率"""
        correct = 0

        for case in test_cases:
            response = self.assistant.process_request(case["input"])
            if case["expected"] in response:
                correct += 1

        return correct / len(test_cases)
```

---

## 部署方案

### Docker部署

```dockerfile
# Dockerfile

FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "main.py"]
```

### 云服务部署

```python
# deploy/cloud.py

"""
云服务部署脚本
"""

import os
from flask import Flask, request, jsonify
from main import IntelligentAssistant

app = Flask(__name__)
assistant = IntelligentAssistant()

@app.route('/api/chat', methods=['POST'])
def chat():
    """聊天API"""
    data = request.json
    user_input = data.get('message', '')

    response = assistant.process_request(user_input)

    return jsonify({
        "response": response
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
```

---

## 项目总结

### 技术亮点

1. ✅ 多智能体协作架构
2. ✅ 模块化设计
3. ✅ 可扩展的工具系统
4. ✅ 完整的文档和测试
5. ✅ 多种部署方案

### 学到的技能

- 🏗️ 系统架构设计
- 🤖 智能体开发
- 🧩 模块化编程
- 📝 文档编写
- 🧪 测试和评估

### 后续改进

- 🌐 Web界面开发
- 📱 移动端适配
- 🌍 多语言支持
- 💾 分布式部署
- 📈 数据分析面板

---

## 提交清单

### 代码
- [x] 完整源代码
- [x] 单元测试
- [x] 配置文件

### 文档
- [x] README.md
- [x] API文档
- [x] 使用指南

### 其他
- [x] requirements.txt
- [x] LICENSE
- [x] .gitignore

---

## 恭喜！🎉

你已经完成了DataWhale《从零开始构建智能体》的全部学习内容！

从ReAct、Plan-and-Solve、Reflection三种经典范式，
到低代码平台、框架开发、记忆检索，
再到多智能体协作、深度研究、赛博小镇模拟，
你现在已经具备了：
- ✅ 扎实的理论基础
- ✅ 丰富的实践经验
- ✅ 独立开发能力

**继续探索，构建更强大的智能体应用吧！**

---

## 许可证

MIT License

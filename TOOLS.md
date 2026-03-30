# 🛠️ 实用工具集

这里收集了在学习过程中开发的一些实用工具。

## 目录

1. [配置管理工具](#配置管理工具)
2. [日志工具](#日志工具)
3. [评估工具](#评估工具)
4. [可视化工具](#可视化工具)

---

## 配置管理工具

### API配置管理器

```python
# tools/config_manager.py

import os
import json
from typing import Dict, Any
from dataclasses import dataclass


@dataclass
class LLMConfig:
    """LLM配置"""
    api_key: str
    model_id: str
    base_url: str
    timeout: int = 60
    temperature: float = 0.7
    max_tokens: int = 2000


class ConfigManager:
    """配置管理器"""

    @staticmethod
    def load_from_env(file_path: str = ".env") -> LLMConfig:
        """从环境变量加载配置"""
        from dotenv import load_dotenv
        load_dotenv(file_path)

        return LLMConfig(
            api_key=os.getenv("LLM_API_KEY"),
            model_id=os.getenv("LLM_MODEL_ID"),
            base_url=os.getenv("LLM_BASE_URL"),
            timeout=int(os.getenv("LLM_TIMEOUT", "60")),
            temperature=float(os.getenv("LLM_TEMPERATURE", "0.7")),
            max_tokens=int(os.getenv("LLM_MAX_TOKENS", "2000"))
        )

    @staticmethod
    def load_from_json(file_path: str) -> Dict[str, Any]:
        """从JSON文件加载配置"""
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    @staticmethod
    def save_to_json(config: Dict, file_path: str):
        """保存配置到JSON文件"""
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
```

---

## 日志工具

### 智能体日志记录器

```python
# tools/agent_logger.py

import logging
from datetime import datetime
from typing import Dict, Any
import json


class AgentLogger:
    """智能体专用日志记录器"""

    def __init__(self, name: str, log_file: str = None):
        self.name = name
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)

        # 控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        # 文件处理器
        if log_file:
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

        # 交互历史
        self.interaction_history = []

    def log_interaction(self, role: str, content: str, metadata: Dict = None):
        """记录交互"""
        interaction = {
            "timestamp": datetime.now().isoformat(),
            "role": role,
            "content": content,
            "metadata": metadata or {}
        }
        self.interaction_history.append(interaction)

        self.logger.info(f"[{role}] {content}")

    def log_tool_use(self, tool_name: str, inputs: Any, outputs: Any):
        """记录工具使用"""
        self.logger.info(f"Tool: {tool_name}")
        self.logger.debug(f"  Inputs: {inputs}")
        self.logger.debug(f"  Outputs: {outputs}")

    def log_error(self, error: Exception, context: str = ""):
        """记录错误"""
        self.logger.error(f"Error in {context}: {str(error)}", exc_info=True)

    def save_history(self, file_path: str):
        """保存交互历史"""
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(self.interaction_history, f, ensure_ascii=False, indent=2)

    def get_statistics(self) -> Dict:
        """获取统计信息"""
        total_interactions = len(self.interaction_history)
        user_messages = len([i for i in self.interaction_history if i["role"] == "user"])
        assistant_messages = len([i for i in self.interaction_history if i["role"] == "assistant"])

        return {
            "total_interactions": total_interactions,
            "user_messages": user_messages,
            "assistant_messages": assistant_messages,
            "first_interaction": self.interaction_history[0]["timestamp"] if self.interaction_history else None,
            "last_interaction": self.interaction_history[-1]["timestamp"] if self.interaction_history else None
        }
```

---

## 评估工具

### 智能体性能测试器

```python
# tools/performance_tester.py

import time
from typing import List, Dict, Callable
import statistics


class PerformanceTester:
    """性能测试器"""

    def __init__(self):
        self.results = []

    def test_response_time(self, agent: Any, test_cases: List[Dict]) -> Dict:
        """测试响应时间"""
        response_times = []

        for case in test_cases:
            start = time.time()
            try:
                agent.process(case["input"])
                end = time.time()
                response_times.append(end - start)
            except Exception as e:
                print(f"Error processing case: {e}")

        if not response_times:
            return {"error": "No successful responses"}

        return {
            "mean": statistics.mean(response_times),
            "median": statistics.median(response_times),
            "stdev": statistics.stdev(response_times) if len(response_times) > 1 else 0,
            "min": min(response_times),
            "max": max(response_times)
        }

    def test_accuracy(self, agent: Any, test_cases: List[Dict]) -> Dict:
        """测试准确率"""
        correct = 0
        total = len(test_cases)

        for case in test_cases:
            try:
                response = agent.process(case["input"])
                if self._check_correctness(response, case.get("expected")):
                    correct += 1
            except Exception as e:
                print(f"Error in accuracy test: {e}")

        return {
            "accuracy": correct / total if total > 0 else 0,
            "correct": correct,
            "total": total
        }

    def test_memory_usage(self, agent: Any) -> Dict:
        """测试内存使用"""
        import psutil
        import os

        process = psutil.Process(os.getpid())
        memory_info = process.memory_info()

        return {
            "rss_mb": memory_info.rss / 1024 / 1024,  # 物理内存
            "vms_mb": memory_info.vms / 1024 / 1024,  # 虚拟内存
            "percent": process.memory_percent()       # 内存使用百分比
        }

    def _check_correctness(self, response: str, expected: str) -> bool:
        """检查回答是否正确（简化实现）"""
        if not expected:
            return True
        return expected.lower() in response.lower()

    def run_benchmark(self, agent: Any, test_cases: List[Dict]) -> Dict:
        """运行完整基准测试"""
        print("🔬 开始性能测试...")
        print("="*50)

        # 1. 响应时间测试
        print("📊 测试响应时间...")
        response_time_stats = self.test_response_time(agent, test_cases)
        print(f"  平均响应时间: {response_time_stats.get('mean', 0):.3f}秒")
        print(f"  最小响应时间: {response_time_stats.get('min', 0):.3f}秒")
        print(f"  最大响应时间: {response_time_stats.get('max', 0):.3f}秒")

        # 2. 准确率测试
        print("\n🎯 测试准确率...")
        accuracy_stats = self.test_accuracy(agent, test_cases)
        print(f"  准确率: {accuracy_stats['accuracy']:.2%}")
        print(f"  正确数: {accuracy_stats['correct']}/{accuracy_stats['total']}")

        # 3. 内存使用测试
        print("\n💾 测试内存使用...")
        memory_stats = self.test_memory_usage(agent)
        print(f"  物理内存: {memory_stats['rss_mb']:.1f}MB")
        print(f"  虚拟内存: {memory_stats['vms_mb']:.1f}MB")
        print(f"  使用率: {memory_stats['percent']:.1f}%")

        print("\n" + "="*50)
        print("✅ 测试完成")

        return {
            "response_time": response_time_stats,
            "accuracy": accuracy_stats,
            "memory": memory_stats
        }
```

---

## 可视化工具

### 智能体行为可视化

```python
# tools/visualizer.py

import matplotlib.pyplot as plt
from typing import List, Dict
import networkx as nx
from datetime import datetime


class AgentVisualizer:
    """智能体行为可视化工具"""

    def plot_response_times(self, response_times: List[float], save_path: str = None):
        """绘制响应时间分布"""
        plt.figure(figsize=(10, 6))
        plt.hist(response_times, bins=20, edgecolor='black')
        plt.xlabel('Response Time (seconds)')
        plt.ylabel('Frequency')
        plt.title('Distribution of Response Times')
        plt.grid(True, alpha=0.3)

        if save_path:
            plt.savefig(save_path)
        plt.show()

    def plot_accuracy_over_time(self, accuracy_history: List[Dict], save_path: str = None):
        """绘制准确率随时间变化"""
        times = [datetime.fromisoformat(h["timestamp"]) for h in accuracy_history]
        accuracies = [h["accuracy"] for h in accuracy_history]

        plt.figure(figsize=(12, 6))
        plt.plot(times, accuracies, marker='o', linestyle='-')
        plt.xlabel('Time')
        plt.ylabel('Accuracy')
        plt.title('Accuracy Over Time')
        plt.grid(True, alpha=0.3)
        plt.xticks(rotation=45)

        if save_path:
            plt.savefig(save_path)
        plt.show()

    def plot_interaction_flow(self, interactions: List[Dict], save_path: str = None):
        """绘制交互流程图"""
        G = nx.DiGraph()

        for interaction in interactions:
            role = interaction["role"]
            G.add_node(role)

            # 添加边（简化实现）
            if role == "user":
                G.add_edge("user", "assistant")

        plt.figure(figsize=(10, 8))
        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, node_size=3000,
                node_color='lightblue', arrowsize=20, font_size=12)

        if save_path:
            plt.savefig(save_path)
        plt.show()

    def plot_token_usage(self, token_history: List[Dict], save_path: str = None):
        """绘制Token使用情况"""
        iterations = range(1, len(token_history) + 1)
        input_tokens = [h["input_tokens"] for h in token_history]
        output_tokens = [h["output_tokens"] for h in token_history]
        total_tokens = [i + o for i, o in zip(input_tokens, output_tokens)]

        fig, ax = plt.subplots(figsize=(12, 6))

        ax.plot(iterations, input_tokens, label='Input Tokens', marker='o')
        ax.plot(iterations, output_tokens, label='Output Tokens', marker='s')
        ax.plot(iterations, total_tokens, label='Total Tokens', marker='^', linestyle='--')

        ax.set_xlabel('Iteration')
        ax.set_ylabel('Number of Tokens')
        ax.set_title('Token Usage Over Iterations')
        ax.legend()
        ax.grid(True, alpha=0.3)

        if save_path:
            plt.savefig(save_path)
        plt.show()
```

---

## 使用示例

```python
# example_tools.py

from tools.config_manager import ConfigManager
from tools.agent_logger import AgentLogger
from tools.performance_tester import PerformanceTester
from tools.visualizer import AgentVisualizer


def main():
    """工具使用示例"""

    # 1. 配置管理
    print("📝 配置管理示例")
    config = ConfigManager.load_from_env()
    print(f"  Model: {config.model_id}")
    print(f"  Base URL: {config.base_url}")

    # 2. 日志记录
    print("\n📊 日志记录示例")
    logger = AgentLogger("test_agent", "agent.log")
    logger.log_interaction("user", "你好")
    logger.log_interaction("assistant", "你好！有什么可以帮助你的？")
    logger.save_history("interaction_history.json")

    # 3. 性能测试
    print("\n🔬 性能测试示例")
    tester = PerformanceTester()

    # 测试用例
    test_cases = [
        {"input": "测试问题1", "expected": "测试答案1"},
        {"input": "测试问题2", "expected": "测试答案2"}
    ]

    # 注意：这里需要一个真实的agent对象
    # benchmark = tester.run_benchmark(your_agent, test_cases)

    # 4. 可视化
    print("\n📈 可视化示例")
    visualizer = AgentVisualizer()

    # 响应时间数据
    response_times = [0.5, 0.7, 0.6, 0.8, 0.4]
    # visualizer.plot_response_times(response_times, "response_times.png")


if __name__ == "__main__":
    main()
```

---

## 安装依赖

```bash
pip install matplotlib networkx psutil
```

---

## 使用建议

1. **配置管理**：统一管理所有API配置
2. **日志记录**：记录智能体的所有交互
3. **性能测试**：定期测试智能体性能
4. **数据可视化**：直观展示智能体行为

---

## 许可证

MIT License

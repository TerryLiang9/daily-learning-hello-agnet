# 第十二章：智能体性能评估

> 核心指标、基准测试与评估框架

**本章重点**：
- 理解智能体评估的重要性
- 掌握核心评估指标
- 构建完整的评估框架

---

## 学习笔记

### 12.1 评估维度

**智能体评估的四大维度**：

```
评估维度
├── 准确性 (Accuracy)
├── 效率 (Efficiency)
├── 鲁棒性 (Robustness)
└── 可解释性 (Interpretability)
```

| 维度 | 指标 | 测量方法 |
|------|------|----------|
| **准确性** | 正确率、F1分数 | 对比标准答案 |
| **效率** | 响应时间、资源消耗 | 性能监控 |
| **鲁棒性** | 抗干扰能力 | 压力测试 |
| **可解释性** | 决策透明度 | 路径追踪 |

### 12.2 常用评估指标

#### 任务完成度
- **成功率**：完成任务的比例
- **完成时间**：平均耗时
- **步骤数**：执行步数

#### 质量指标
- **精确率**：结果准确度
- **召回率**：信息完整性
- **F1分数**：综合评估

#### 资源消耗
- **Token使用量**：LLM调用成本
- **API调用次数**：网络开销
- **内存占用**：系统资源

---

## 实现代码

### 1. 评估指标计算

```python
# metrics.py

from typing import List, Dict, Any
from collections import Counter
import time


class MetricsCalculator:
    """评估指标计算器"""

    @staticmethod
    def accuracy(predictions: List[str], ground_truth: List[str]) -> float:
        """计算准确率"""
        correct = sum(1 for p, g in zip(predictions, ground_truth) if p == g)
        return correct / len(predictions) if predictions else 0.0

    @staticmethod
    def precision_recall_f1(true_positives: int,
                           false_positives: int,
                           false_negatives: int) -> Dict[str, float]:
        """计算精确率、召回率、F1分数"""
        precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0.0
        recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0.0
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0

        return {
            "precision": precision,
            "recall": recall,
            "f1": f1
        }

    @staticmethod
    def success_rate(tasks: List[Dict[str, Any]]) -> float:
        """计算任务成功率"""
        successful = sum(1 for task in tasks if task.get("success", False))
        return successful / len(tasks) if tasks else 0.0

    @staticmethod
    def average_completion_time(tasks: List[Dict[str, Any]]) -> float:
        """计算平均完成时间"""
        times = [task.get("completion_time", 0) for task in tasks if task.get("success", False)]
        return sum(times) / len(times) if times else 0.0

    @staticmethod
    def average_steps(tasks: List[Dict[str, Any]]) -> float:
        """计算平均执行步数"""
        steps = [task.get("steps", 0) for task in tasks if task.get("success", False)]
        return sum(steps) / len(steps) if steps else 0.0


class TokenTracker:
    """Token使用量追踪"""

    def __init__(self):
        self.total_input_tokens = 0
        self.total_output_tokens = 0
        self.api_calls = 0

    def log_call(self, input_tokens: int, output_tokens: int):
        """记录API调用"""
        self.total_input_tokens += input_tokens
        self.total_output_tokens += output_tokens
        self.api_calls += 1

    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        return {
            "total_input_tokens": self.total_input_tokens,
            "total_output_tokens": self.total_output_tokens,
            "total_tokens": self.total_input_tokens + self.total_output_tokens,
            "api_calls": self.api_calls,
            "avg_tokens_per_call": (self.total_input_tokens + self.total_output_tokens) / self.api_calls if self.api_calls > 0 else 0
        }

    def estimate_cost(self, input_price_per_1k: float = 0.001,
                     output_price_per_1k: float = 0.002) -> float:
        """估算成本（美元）"""
        input_cost = (self.total_input_tokens / 1000) * input_price_per_1k
        output_cost = (self.total_output_tokens / 1000) * output_price_per_1k
        return input_cost + output_cost
```

### 2. 评估框架

```python
# evaluation_framework.py

from typing import List, Dict, Any, Callable
from metrics import MetricsCalculator, TokenTracker
import time


class EvaluationFramework:
    """智能体评估框架"""

    def __init__(self, agent: Any):
        self.agent = agent
        self.metrics_calculator = MetricsCalculator()
        self.token_tracker = TokenTracker()
        self.results = []

    def evaluate_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """评估单个任务"""
        start_time = time.time()

        # 执行任务
        try:
            result = self.agent.run(task["input"])
            success = task["check_func"](result) if "check_func" in task else True
        except Exception as e:
            result = None
            success = False

        end_time = time.time()

        # 记录结果
        task_result = {
            "task_id": task.get("id", ""),
            "input": task["input"],
            "expected_output": task.get("expected_output"),
            "actual_output": result,
            "success": success,
            "completion_time": end_time - start_time,
            "steps": task.get("steps", 0)
        }

        self.results.append(task_result)
        return task_result

    def evaluate_batch(self, tasks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """批量评估任务"""
        print(f"开始评估 {len(tasks)} 个任务...")

        for i, task in enumerate(tasks, 1):
            print(f"进度: {i}/{len(tasks)}")
            self.evaluate_task(task)

        # 生成报告
        report = self.generate_report()
        return report

    def generate_report(self) -> Dict[str, Any]:
        """生成评估报告"""
        if not self.results:
            return {}

        # 基础统计
        success_rate = self.metrics_calculator.success_rate(self.results)
        avg_time = self.metrics_calculator.average_completion_time(self.results)
        avg_steps = self.metrics_calculator.average_steps(self.results)

        # Token统计
        token_stats = self.token_tracker.get_stats()
        estimated_cost = self.token_tracker.estimate_cost()

        # 详细结果
        successful_tasks = [r for r in self.results if r["success"]]
        failed_tasks = [r for r in self.results if not r["success"]]

        report = {
            "summary": {
                "total_tasks": len(self.results),
                "successful_tasks": len(successful_tasks),
                "failed_tasks": len(failed_tasks),
                "success_rate": success_rate,
                "average_completion_time": avg_time,
                "average_steps": avg_steps
            },
            "token_usage": {
                **token_stats,
                "estimated_cost_usd": estimated_cost
            },
            "failed_tasks": [
                {
                    "task_id": t["task_id"],
                    "input": t["input"],
                    "expected": t.get("expected_output"),
                    "actual": t["actual_output"]
                }
                for t in failed_tasks
            ],
            "successful_tasks": [
                {
                    "task_id": t["task_id"],
                    "input": t["input"],
                    "completion_time": t["completion_time"]
                }
                for t in successful_tasks
            ]
        }

        return report

    def print_report(self, report: Dict[str, Any]):
        """打印评估报告"""
        print("\n" + "="*50)
        print("评估报告")
        print("="*50)

        # 摘要
        print("\n【摘要】")
        for key, value in report["summary"].items():
            if isinstance(value, float):
                print(f"{key}: {value:.4f}")
            else:
                print(f"{key}: {value}")

        # Token使用
        print("\n【Token使用】")
        for key, value in report["token_usage"].items():
            if isinstance(value, float):
                print(f"{key}: {value:.4f}")
            else:
                print(f"{key}: {value}")

        # 失败任务
        if report["summary"]["failed_tasks"] > 0:
            print("\n【失败任务】")
            for task in report["failed_tasks"]:
                print(f"- 任务 {task['task_id']}: {task['input']}")
                print(f"  期望: {task.get('expected', 'N/A')}")
                print(f"  实际: {task.get('actual', 'N/A')}")

        print("\n" + "="*50)
```

### 3. 使用示例

```python
# example_evaluation.py

from evaluation_framework import EvaluationFramework
from react_agent import ReActAgent
from llm_client import HelloAgentsLLM
from tools import ToolExecutor, search


def main():
    # 初始化智能体
    llm_client = HelloAgentsLLM()
    tool_executor = ToolExecutor()
    tool_executor.registerTool("Search", "搜索工具", search)
    agent = ReActAgent(llm_client, tool_executor)

    # 创建评估框架
    framework = EvaluationFramework(agent)

    # 定义测试任务
    test_tasks = [
        {
            "id": "task_1",
            "input": "华为最新的手机是哪一款？",
            "check_func": lambda x: x is not None and len(x) > 10
        },
        {
            "id": "task_2",
            "input": "英伟达最新的GPU型号是什么？",
            "check_func": lambda x: x is not None and "GPU" in x
        },
        {
            "id": "task_3",
            "input": "2024年AI领域有什么重要突破？",
            "check_func": lambda x: x is not None and len(x) > 20
        }
    ]

    # 运行评估
    report = framework.evaluate_batch(test_tasks)

    # 打印报告
    framework.print_report(report)

    # 保存报告
    import json
    with open("evaluation_report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
```

---

## 实践项目

### 项目：智能Agent基准测试套件

```python
# agent_benchmark.py

from typing import List, Dict
from evaluation_framework import EvaluationFramework


class AgentBenchmark:
    """智能体基准测试"""

    def __init__(self):
        self.test_suites = {}

    def register_suite(self, name: str, tasks: List[Dict]):
        """注册测试套件"""
        self.test_suites[name] = tasks

    def run_suite(self, agent: Any, suite_name: str) -> Dict:
        """运行测试套件"""
        if suite_name not in self.test_suites:
            raise ValueError(f"测试套件 {suite_name} 不存在")

        framework = EvaluationFramework(agent)
        return framework.evaluate_batch(self.test_suites[suite_name])

    def compare_agents(self, agents: Dict[str, Any], suite_name: str) -> Dict:
        """比较多个智能体"""
        results = {}

        for agent_name, agent in agents.items():
            print(f"\n评估智能体: {agent_name}")
            results[agent_name] = self.run_suite(agent, suite_name)

        return results


# 预定义测试套件
def create_reasoning_suite() -> List[Dict]:
    """创建推理测试套件"""
    return [
        {
            "id": "math_1",
            "input": "一个水果店周一卖出15个苹果，周二卖出周一的两倍，周三比周二少5个，总共卖出多少？",
            "expected_output": "70",
            "check_func": lambda x: "70" in str(x)
        },
        {
            "id": "logic_1",
            "input": "如果所有的A都是B，所有的B都是C，那么所有的A都是C吗？",
            "expected_output": "是",
            "check_func": lambda x: "是" in str(x)
        }
    ]


def create_retrieval_suite() -> List[Dict]:
    """创建检索测试套件"""
    return [
        {
            "id": "search_1",
            "input": "搜索最新的GPT模型信息",
            "check_func": lambda x: x is not None and len(x) > 20
        },
        {
            "id": "search_2",
            "input": "查找Python最新版本",
            "check_func": lambda x: x is not None and ("Python" in x or "python" in x)
        }
    ]


# 使用示例
if __name__ == "__main__":
    # 创建基准测试
    benchmark = AgentBenchmark()

    # 注册测试套件
    benchmark.register_suite("reasoning", create_reasoning_suite())
    benchmark.register_suite("retrieval", create_retrieval_suite())

    # 比较不同智能体（示例）
    agents = {
        "react_agent": None,  # 实际应用中替换为真实agent
        "plan_solve_agent": None
    }

    # 运行比较
    # results = benchmark.compare_agents(agents, "reasoning")
```

---

## 学习总结

### 评估最佳实践

1. **多维度评估**：不只看准确率
2. **真实场景**：使用实际任务测试
3. **持续监控**：建立监控体系
4. **A/B测试**：对比不同版本

### 常见基准数据集

- **MMLU**：综合知识评估
- **GSM8K**：数学问题
- **HumanEval**：代码生成
- **BBH**：推理能力

---

## 参考资源

- [LangChain Evaluation](https://python.langchain.com/docs/guides/evaluation/)
- [Prompt Engineering Guide](https://www.promptingguide.ai/)
- [LLM Benchmarking](https://huggingface.co/spaces/HuggingFaceH4/open_llm_leaderboard)

---

## 许可证

MIT License

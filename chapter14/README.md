# 第十四章：自动化深度研究智能体

> DeepResearch Agent 复现与解析

**本章目标**：
- 理解深度研究智能体的工作原理
- 实现自动化研究系统
- 掌握复杂任务的分解与执行

---

## 项目概述

### 什么是深度研究智能体？

**DeepResearch Agent** 是一个能够：
- 🔍 自动搜索和收集信息
- 📚 分析多个来源的资料
- 📝 生成综合研究报告
- 🔄 迭代优化研究质量

### 核心能力

```
深度研究能力
├── 信息检索 - 从多个来源获取数据
├── 内容分析 - 理解和提取关键信息
├── 交叉验证 - 对比多个来源
├── 综合总结 - 生成连贯报告
└── 质量评估 - 评估研究完整性
```

---

## 系统设计

### 架构图

```
┌─────────────────────────────────────────┐
│          研究协调器 (Coordinator)        │
├─────────────────────────────────────────┤
│  - 任务分解                              │
│  - 进度管理                              │
│  - 质量控制                              │
└─────────────────────────────────────────┘
                    │
    ┌───────────────┼───────────────┐
    │               │               │
┌───▼───┐     ┌───▼───┐     ┌───▼───┐
│搜索   │     │分析   │     │写作   │
│智能体 │     │智能体 │     │智能体 │
└───────┘     └───────┘     └───────┘
    │               │               │
    └───────────────┴───────────────┘
                    │
            ┌───────▼────────┐
            │   工具层        │
            │ - 搜索引擎      │
            │ - 网页抓取      │
            │ - 向量数据库    │
            └────────────────┘
```

---

## 实现代码

### 1. 研究任务定义

```python
# research_task.py

from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum


class TaskStatus(Enum):
    """任务状态"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class ResearchQuestion:
    """研究问题"""
    question: str
    sub_questions: List[str] = None
    keywords: List[str] = None
    status: TaskStatus = TaskStatus.PENDING
    findings: List[str] = None

    def __post_init__(self):
        if self.sub_questions is None:
            self.sub_questions = []
        if self.keywords is None:
            self.keywords = []
        if self.findings is None:
            self.findings = []


@dataclass
class Source:
    """信息来源"""
    url: str
    title: str
    content: str
    credibility_score: float = 0.5
    relevance_score: float = 0.5


@dataclass
class ResearchReport:
    """研究报告"""
    topic: str
    introduction: str
    key_findings: List[str]
    detailed_analysis: Dict[str, str]
    conclusion: str
    sources: List[Source]
    confidence_level: float = 0.0
```

### 2. 搜索智能体

```python
# search_agent.py

from typing import List, Dict
from research_task import Source
import requests
from bs4 import BeautifulSoup


class SearchAgent:
    """搜索智能体 - 负责信息收集"""

    def __init__(self, search_api_key: str = None):
        self.search_api_key = search_api_key
        self.sources = []

    def search(self, query: str, num_results: int = 10) -> List[Dict]:
        """执行搜索"""
        print(f"🔍 搜索: {query}")

        # 这里使用模拟数据，实际应用中应该调用真实API
        # 例如：Google Search API, Bing Search API等
        results = self._mock_search(query, num_results)

        for result in results:
            print(f"  ✓ {result['title']}")

        return results

    def _mock_search(self, query: str, num_results: int) -> List[Dict]:
        """模拟搜索（实际应用中替换为真实API）"""
        return [
            {
                "title": f"{query} - 维基百科",
                "url": f"https://example.com/{query}",
                "snippet": f"关于{query}的详细介绍..."
            },
            {
                "title": f"{query}最新研究",
                "url": f"https://research.example.com/{query}",
                "snippet": f"{query}的最新研究进展..."
            }
        ]

    def fetch_content(self, url: str) -> str:
        """获取网页内容"""
        print(f"📥 获取内容: {url}")

        try:
            # 模拟获取内容
            return f"从 {url} 获取的内容..."
        except Exception as e:
            print(f"❌ 获取失败: {e}")
            return ""

    def extract_key_info(self, content: str, query: str) -> str:
        """提取关键信息"""
        # 简化实现
        lines = content.split("\n")
        key_lines = [line for line in lines if len(line) > 20][:5]
        return "\n".join(key_lines)

    def search_and_collect(self, queries: List[str]) -> List[Source]:
        """搜索并收集信息"""
        all_sources = []

        for query in queries:
            # 搜索
            results = self.search(query)

            # 收集内容
            for result in results:
                content = self.fetch_content(result["url"])

                source = Source(
                    url=result["url"],
                    title=result["title"],
                    content=content,
                    credibility_score=0.7,  # 简化实现
                    relevance_score=0.8
                )

                all_sources.append(source)

        return all_sources
```

### 3. 分析智能体

```python
# analysis_agent.py

from typing import List, Dict
from research_task import Source, ResearchQuestion
from llm_client import HelloAgentsLLM


class AnalysisAgent:
    """分析智能体 - 负责内容分析和综合"""

    def __init__(self, llm_client: HelloAgentsLLM):
        self.llm_client = llm_client

    def analyze_sources(self, sources: List[Source], question: str) -> Dict:
        """分析信息来源"""
        print(f"\n🔬 分析 {len(sources)} 个来源...")

        # 提取关键信息
        key_findings = []

        for i, source in enumerate(sources, 1):
            print(f"  分析来源 {i}/{len(sources)}: {source.title}")

            finding = self._extract_finding(source, question)
            key_findings.append(finding)

        # 综合分析
        synthesis = self._synthesize_findings(key_findings, question)

        return {
            "key_findings": key_findings,
            "synthesis": synthesis,
            "confidence": self._calculate_confidence(sources)
        }

    def _extract_finding(self, source: Source, question: str) -> str:
        """从来源中提取发现"""
        prompt = f"""
基于以下来源，提取关于"{question}"的关键信息：

来源标题：{source.title}
内容：{source.content[:500]}

请提取：
1. 主要观点
2. 关键数据
3. 重要结论

返回格式化的发现。
"""

        response = self.llm_client.think([{"role": "user", "content": prompt}])
        return response

    def _synthesize_findings(self, findings: List[str], question: str) -> str:
        """综合多个发现"""
        findings_text = "\n\n".join([f"{i+1}. {f}" for i, f in enumerate(findings)])

        prompt = f"""
综合以下研究发现，关于"{question}"的结论：

{findings_text}

请生成：
1. 共识观点
2. 争议点（如果有）
3. 主要结论
"""

        response = self.llm_client.think([{"role": "user", "content": prompt}])
        return response

    def _calculate_confidence(self, sources: List[Source]) -> float:
        """计算置信度"""
        if not sources:
            return 0.0

        # 基于来源可信度和相关性计算
        total_score = sum(s.credibility_score * s.relevance_score for s in sources)
        avg_score = total_score / len(sources)

        return min(avg_score, 1.0)

    def cross_validate(self, sources: List[Source], claim: str) -> Dict:
        """交叉验证声明"""
        print(f"\n✓ 交叉验证: {claim}")

        supporting = []
        contradicting = []
        neutral = []

        for source in sources:
            # 简化实现：检查内容是否包含相关关键词
            if claim.lower() in source.content.lower():
                supporting.append(source.title)
            else:
                neutral.append(source.title)

        return {
            "claim": claim,
            "supporting_count": len(supporting),
            "contradicting_count": len(contradicting),
            "validation": "支持" if len(supporting) > len(sources)/2 else "中立"
        }
```

### 4. 写作智能体

```python
# writing_agent.py

from typing import List, Dict
from research_task import ResearchReport, Source
from llm_client import HelloAgentsLLM


class WritingAgent:
    """写作智能体 - 负责生成研究报告"""

    def __init__(self, llm_client: HelloAgentsLLM):
        self.llm_client = llm_client

    def generate_report(self, topic: str, analysis: Dict, sources: List[Source]) -> ResearchReport:
        """生成完整报告"""
        print(f"\n📝 生成报告: {topic}")

        # 1. 引言
        introduction = self._write_introduction(topic, analysis)

        # 2. 主要发现
        key_findings = analysis["key_findings"]

        # 3. 详细分析
        detailed_analysis = self._write_detailed_analysis(analysis)

        # 4. 结论
        conclusion = self._write_conclusion(analysis)

        # 5. 创建报告对象
        report = ResearchReport(
            topic=topic,
            introduction=introduction,
            key_findings=key_findings,
            detailed_analysis=detailed_analysis,
            conclusion=conclusion,
            sources=sources,
            confidence_level=analysis["confidence"]
        )

        return report

    def _write_introduction(self, topic: str, analysis: Dict) -> str:
        """写引言"""
        prompt = f"""
为研究主题"{topic}"写一个引言。

综合分析：{analysis['synthesis'][:200]}

引言应包括：
1. 研究背景
2. 研究重要性
3. 报告结构概述

请写一个200-300字的引言。
"""

        return self.llm_client.think([{"role": "user", "content": prompt}])

    def _write_detailed_analysis(self, analysis: Dict) -> Dict[str, str]:
        """写详细分析"""
        sections = {}

        # 为每个关键发现创建详细章节
        for i, finding in enumerate(analysis["key_findings"]):
            section_title = f"发现 {i+1}"
            section_content = self._expand_finding(finding)
            sections[section_title] = section_content

        return sections

    def _expand_finding(self, finding: str) -> str:
        """扩展发现内容"""
        prompt = f"""
将以下研究发现扩展成详细的段落：

{finding}

请提供：
1. 详细解释
2. 支持证据
3. 实际意义

生成150-200字的段落。
"""

        return self.llm_client.think([{"role": "user", "content": prompt}])

    def _write_conclusion(self, analysis: Dict) -> str:
        """写结论"""
        prompt = f"""
基于以下综合分析写一个结论：

{analysis['synthesis']}

结论应包括：
1. 主要结论总结
2. 研究局限性
3. 未来研究方向

请写一个150-200字的结论。
"""

        return self.llm_client.think([{"role": "user", "content": prompt}])

    def format_report(self, report: ResearchReport) -> str:
        """格式化报告为Markdown"""
        md = f"# {report.topic}\n\n"
        md += f"## 引言\n\n{report.introduction}\n\n"
        md += f"## 主要发现\n\n"

        for i, finding in enumerate(report.key_findings, 1):
            md += f"{i}. {finding}\n\n"

        md += f"## 详细分析\n\n"

        for section, content in report.detailed_analysis.items():
            md += f"### {section}\n\n{content}\n\n"

        md += f"## 结论\n\n{report.conclusion}\n\n"
        md += f"## 参考文献\n\n"

        for source in report.sources:
            md += f"- [{source.title}]({source.url})\n"

        md += f"\n\n*置信度: {report.confidence_level:.2%}*"

        return md
```

### 5. 研究协调器

```python
# research_coordinator.py

from typing import List
from research_task import ResearchQuestion, ResearchReport
from search_agent import SearchAgent
from analysis_agent import AnalysisAgent
from writing_agent import WritingAgent
from llm_client import HelloAgentsLLM


class ResearchCoordinator:
    """研究协调器 - 整合所有智能体"""

    def __init__(self, llm_client: HelloAgentsLLM):
        self.llm_client = llm_client
        self.search_agent = SearchAgent()
        self.analysis_agent = AnalysisAgent(llm_client)
        self.writing_agent = WritingAgent(llm_client)

    def conduct_research(self, topic: str, depth: int = 3) -> ResearchReport:
        """执行深度研究"""
        print("\n" + "="*50)
        print("🔬 深度研究智能体")
        print("="*50)
        print(f"\n研究主题: {topic}")
        print(f"研究深度: {depth}层\n")

        # 阶段1: 分解研究问题
        research_questions = self._decompose_topic(topic, depth)
        print(f"✓ 生成 {len(research_questions)} 个研究问题\n")

        # 阶段2: 搜索和收集信息
        print("="*50)
        print("📚 阶段1: 信息收集")
        print("="*50)

        all_sources = []
        for question in research_questions:
            queries = [question.question] + question.keywords
            sources = self.search_agent.search_and_collect(queries)
            all_sources.extend(sources)

        print(f"\n✓ 收集到 {len(all_sources)} 个信息来源\n")

        # 阶段3: 分析信息
        print("="*50)
        print("🔬 阶段2: 深度分析")
        print("="*50)

        analysis = self.analysis_agent.analyze_sources(all_sources, topic)

        # 阶段4: 生成报告
        print("\n" + "="*50)
        print("📝 阶段3: 报告生成")
        print("="*50)

        report = self.writing_agent.generate_report(topic, analysis, all_sources)

        print("\n" + "="*50)
        print("✅ 研究完成！")
        print("="*50)

        return report

    def _decompose_topic(self, topic: str, depth: int) -> List[ResearchQuestion]:
        """分解研究主题"""
        prompt = f"""
将研究主题"{topic}"分解为{depth}个具体的子问题。

要求：
1. 每个子问题应该是可研究的
2. 子问题之间应该有逻辑关联
3. 生成相应的搜索关键词

请返回问题列表。
"""

        response = self.llm_client.think([{"role": "user", "content": prompt}])

        # 简化实现：手动创建问题
        questions = [
            ResearchQuestion(
                question=f"{topic}的基本概念和定义",
                keywords=["什么是", "定义", "概念"]
            ),
            ResearchQuestion(
                question=f"{topic}的最新发展和趋势",
                keywords=["最新", "发展", "趋势", "2024"]
            ),
            ResearchQuestion(
                question=f"{topic}的应用和影响",
                keywords=["应用", "影响", "案例"]
            )
        ]

        return questions

    def iterative_refinement(self, topic: str, max_iterations: int = 3) -> ResearchReport:
        """迭代优化研究"""
        print("\n🔄 使用迭代优化模式...")

        best_report = None
        best_confidence = 0.0

        for iteration in range(max_iterations):
            print(f"\n--- 第 {iteration + 1} 轮迭代 ---")

            # 执行研究
            report = self.conduct_research(topic, depth=2)

            # 评估质量
            if report.confidence_level > best_confidence:
                best_report = report
                best_confidence = report.confidence_level

            # 如果质量足够好，提前结束
            if report.confidence_level > 0.8:
                print(f"\n✅ 研究质量达标（置信度: {report.confidence_level:.2%}）")
                break

        return best_report
```

### 6. 使用示例

```python
# deep_research_main.py

from research_coordinator import ResearchCoordinator
from writing_agent import WritingAgent
from llm_client import HelloAgentsLLM


def main():
    """主函数"""
    # 初始化
    llm_client = HelloAgentsLLM()
    coordinator = ResearchCoordinator(llm_client)

    # 执行研究
    topic = "人工智能在医疗领域的应用"
    report = coordinator.conduct_research(topic, depth=3)

    # 格式化并保存报告
    writing_agent = WritingAgent(llm_client)
    markdown_report = writing_agent.format_report(report)

    # 保存到文件
    filename = f"{topic.replace(' ', '_')}_研究报告.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(markdown_report)

    print(f"\n📄 报告已保存: {filename}")
    print(f"📊 研究置信度: {report.confidence_level:.2%}\n")

    return report


if __name__ == "__main__":
    main()
```

---

## 项目总结

### 技术亮点

1. **模块化设计** - 清晰的职责划分
2. **多智能体协作** - 搜索、分析、写作分工
3. **迭代优化** - 持续提升研究质量
4. **可配置深度** - 灵活控制研究规模

### 核心优势

- ✅ 全自动化研究流程
- ✅ 多源信息整合
- ✅ 交叉验证机制
- ✅ 高质量报告生成
- ✅ 可扩展架构

### 应用场景

- 📚 学术研究辅助
- 📊 市场调研分析
- 📰 新闻深度报道
- 🔍 技术调研评估
- 📖 知识库构建

---

## 参考资源

- [Multi-Agent Research](https://arxiv.org/abs/2305.14314)
- [AutoGen Research Agents](https://microsoft.github.io/autogen/blog/2023/11/09/AgentChat/)
- [Research-oriented AI](https://www.paperswithcode.com/)

---

## 许可证

MIT License

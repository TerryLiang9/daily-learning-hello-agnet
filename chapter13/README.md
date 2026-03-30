# 第十三章：智能旅行助手

> MCP与多智能体协作的真实世界应用

**本章目标**：
- 将所学知识融会贯通
- 构建一个完整的智能旅行助手系统
- 实践多智能体协作

---

## 项目概述

### 功能需求

**智能旅行助手**需要具备以下能力：

1. ✈️ **行程规划** - 根据用户需求制定旅行计划
2. 🌤️ **天气查询** - 获取目的地天气信息
3. 🏛️ **景点推荐** - 推荐当地旅游景点
4. 📅 **日程安排** - 生成详细的每日行程
5. 💰 **预算估算** - 计算旅行费用
6. 🗺️ **地图服务** - 提供路线规划

### 系统架构

```
智能旅行助手系统
├── 用户交互层 (UI)
├── 协调层 (Coordinator)
├── 专业智能体层
│   ├── 天气智能体
│   ├── 景点智能体
│   ├── 预算智能体
│   └── 行程智能体
└── 工具层 (Tools/API)
```

---

## 实现代码

### 1. 核心智能体实现

```python
# travel_agents.py

from typing import Dict, List, Optional
from abc import ABC, abstractmethod
from llm_client import HelloAgentsLLM


class BaseTravelAgent(ABC):
    """旅行智能体基类"""

    def __init__(self, name: str, llm_client: HelloAgentsLLM):
        self.name = name
        self.llm_client = llm_client
        self.memory = {}

    @abstractmethod
    def handle(self, task: str, context: Dict) -> Dict:
        """处理任务"""
        pass


class WeatherAgent(BaseTravelAgent):
    """天气查询智能体"""

    def handle(self, task: str, context: Dict) -> Dict:
        """查询天气信息"""
        destination = context.get("destination", "")
        dates = context.get("dates", "")

        prompt = f"""
查询{destination}在{dates}期间的天气预报。
请提供：
1. 温度范围
2. 天气状况（晴/雨/阴等）
3. 出行建议

返回格式化的天气报告。
"""

        response = self.llm_client.think([{"role": "user", "content": prompt}])

        return {
            "agent": self.name,
            "task": "weather_query",
            "result": response
        }


class AttractionAgent(BaseTravelAgent):
    """景点推荐智能体"""

    def handle(self, task: str, context: Dict) -> Dict:
        """推荐景点"""
        destination = context.get("destination", "")
        duration = context.get("duration", 3)
        preferences = context.get("preferences", "一般")

        prompt = f"""
为用户推荐{destination}的旅游景点。
行程天数：{duration}天
用户偏好：{preferences}

请推荐：
1. 必游景点（3-5个）
2. 每个景点的特色
3. 推荐游览时间
4. 门票价格（如果知道）

生成结构化的推荐列表。
"""

        response = self.llm_client.think([{"role": "user", "content": prompt}])

        return {
            "agent": self.name,
            "task": "attraction_recommendation",
            "result": response
        }


class BudgetAgent(BaseTravelAgent):
    """预算估算智能体"""

    def handle(self, task: str, context: Dict) -> Dict:
        """估算旅行预算"""
        destination = context.get("destination", "")
        duration = context.get("duration", 3)
        people_count = context.get("people_count", 1)

        prompt = f"""
估算{destination}{duration}天的旅行预算。
人数：{people_count}人

请详细列出：
1. 交通费用（往返+当地）
2. 住宿费用
3. 餐饮费用
4. 景点门票
5. 其他费用（购物、娱乐等）

提供总预算预估和人均预算。
"""

        response = self.llm_client.think([{"role": "user", "content": prompt}])

        return {
            "agent": self.name,
            "task": "budget_estimation",
            "result": response
        }


class ItineraryAgent(BaseTravelAgent):
    """行程规划智能体"""

    def handle(self, task: str, context: Dict) -> Dict:
        """生成详细行程"""
        destination = context.get("destination", "")
        duration = context.get("duration", 3)
        attractions = context.get("attractions", "")
        weather = context.get("weather", "")

        prompt = f"""
为用户规划{destination}{duration}天的详细行程。

已知信息：
- 景点推荐：{attractions}
- 天气情况：{weather}

请生成：
1. 每日行程安排（上午、下午、晚上）
2. 景点游览顺序
3. 用餐建议
4. 交通方式

生成易于跟随的时间表格式行程。
"""

        response = self.llm_client.think([{"role": "user", "content": prompt}])

        return {
            "agent": self.name,
            "task": "itinerary_planning",
            "result": response
        }
```

### 2. 协调器实现

```python
# travel_coordinator.py

from typing import Dict, List
from travel_agents import (
    WeatherAgent,
    AttractionAgent,
    BudgetAgent,
    ItineraryAgent
)
from llm_client import HelloAgentsLLM


class TravelCoordinator:
    """旅行协调器 - 整合多个智能体"""

    def __init__(self, llm_client: HelloAgentsLLM):
        self.llm_client = llm_client

        # 初始化专业智能体
        self.weather_agent = WeatherAgent("天气助手", llm_client)
        self.attraction_agent = AttractionAgent("景点助手", llm_client)
        self.budget_agent = BudgetAgent("预算助手", llm_client)
        self.itinerary_agent = ItineraryAgent("行程助手", llm_client)

        self.agents = {
            "weather": self.weather_agent,
            "attraction": self.attraction_agent,
            "budget": self.budget_agent,
            "itinerary": self.itinerary_agent
        }

    def plan_trip(self, user_request: Dict) -> Dict:
        """规划完整旅行"""
        print("\n" + "="*50)
        print("🌍 智能旅行助手 - 开始规划")
        print("="*50)

        # 提取用户需求
        destination = user_request.get("destination", "北京")
        duration = user_request.get("duration", 3)
        dates = user_request.get("dates", "下个月")
        preferences = user_request.get("preferences", "文化历史")
        people_count = user_request.get("people_count", 1)

        print(f"\n📋 用户需求：")
        print(f"  目的地：{destination}")
        print(f"  天数：{duration}天")
        print(f"  时间：{dates}")
        print(f"  偏好：{preferences}")
        print(f"  人数：{people_count}人")

        # 准备上下文
        context = {
            "destination": destination,
            "duration": duration,
            "dates": dates,
            "preferences": preferences,
            "people_count": people_count
        }

        # 第一阶段：并行查询基础信息
        print(f"\n{'='*50}")
        print("📊 第一阶段：收集基础信息")
        print(f"{'='*50}")

        # 查询天气
        print("\n🌤️ 查询天气...")
        weather_result = self.weather_agent.handle("query", context)
        print(f"✅ {weather_result['result'][:100]}...")
        context["weather"] = weather_result["result"]

        # 推荐景点
        print("\n🏛️ 推荐景点...")
        attraction_result = self.attraction_agent.handle("recommend", context)
        print(f"✅ {attraction_result['result'][:100]}...")
        context["attractions"] = attraction_result["result"]

        # 第二阶段：估算预算和规划行程
        print(f"\n{'='*50}")
        print("📊 第二阶段：制定详细方案")
        print(f"{'='*50}")

        # 估算预算
        print("\n💰 估算预算...")
        budget_result = self.budget_agent.handle("estimate", context)
        print(f"✅ {budget_result['result'][:100]}...")

        # 生成行程
        print("\n📅 生成详细行程...")
        itinerary_result = self.itinerary_agent.handle("plan", context)
        print(f"✅ 行程生成完成")

        # 第三阶段：整合报告
        print(f"\n{'='*50}")
        print("📊 第三阶段：生成旅行计划")
        print(f"{'='*50}")

        travel_plan = self._generate_final_report({
            "weather": weather_result,
            "attractions": attraction_result,
            "budget": budget_result,
            "itinerary": itinerary_result
        }, context)

        print(f"\n{'='*50}")
        print("✅ 旅行计划生成完成！")
        print(f"{'='*50}\n")

        return travel_plan

    def _generate_final_report(self, results: Dict, context: Dict) -> Dict:
        """生成最终报告"""
        prompt = f"""
基于以下信息，生成一份完整、专业的旅行计划报告：

目的地：{context['destination']}
天数：{context['duration']}天
天数：{context['dates']}

## 天气信息
{results['weather']['result']}

## 景点推荐
{results['attractions']['result']}

## 预算估算
{results['budget']['result']}

## 详细行程
{results['itinerary']['result']}

请将以上信息整合成一份结构清晰、易于阅读的旅行计划，包括：
1. 行程概览
2. 每日详细安排
3. 预算明细
4. 温馨提示和注意事项

使用markdown格式输出。
"""

        report = self.llm_client.think([{"role": "user", "content": prompt}])

        return {
            "destination": context['destination'],
            "duration": context['duration'],
            "dates": context['dates'],
            "full_report": report,
            "details": results
        }
```

### 3. 使用示例

```python
# travel_assistant_main.py

from travel_coordinator import TravelCoordinator
from llm_client import HelloAgentsLLM


def main():
    """主函数"""
    print("\n🌍 欢迎使用智能旅行助手！")

    # 初始化
    llm_client = HelloAgentsLLM()
    coordinator = TravelCoordinator(llm_client)

    # 用户需求（实际应用中可以从UI或对话获取）
    user_request = {
        "destination": "杭州",
        "duration": 3,
        "dates": "下周",
        "preferences": "自然风光和历史文化",
        "people_count": 2
    }

    # 生成旅行计划
    travel_plan = coordinator.plan_trip(user_request)

    # 打印完整报告
    print("\n" + "="*50)
    print("📄 完整旅行计划")
    print("="*50)
    print(travel_plan["full_report"])
    print("\n" + "="*50)
    print("✨ 祝您旅途愉快！")
    print("="*50 + "\n")

    return travel_plan


if __name__ == "__main__":
    main()
```

---

## 系统扩展

### 添加地图服务

```python
# map_service.py

import requests


class MapService:
    """地图服务集成"""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://maps.googleapis.com/maps/api"

    def get_route(self, origin: str, destination: str) -> Dict:
        """获取路线规划"""
        url = f"{self.base_url}/directions/json"
        params = {
            "origin": origin,
            "destination": destination,
            "key": self.api_key
        }

        response = requests.get(url, params=params)
        return response.json()

    def search_nearby(self, location: str, place_type: str) -> List[Dict]:
        """搜索附近地点"""
        url = f"{self.base_url}/place/nearbysearch/json"
        params = {
            "location": location,
            "type": place_type,
            "key": self.api_key
        }

        response = requests.get(url, params=params)
        return response.json().get("results", [])
```

### 添加对话接口

```python
# travel_chatbot.py

from travel_coordinator import TravelCoordinator
from llm_client import HelloAgentsLLM
import re


class TravelChatbot:
    """旅行助手聊天机器人"""

    def __init__(self):
        self.llm_client = HelloAgentsLLM()
        self.coordinator = TravelCoordinator(self.llm_client)
        self.conversation_history = []

    def chat(self, user_input: str) -> str:
        """与用户对话"""
        # 添加到历史
        self.conversation_history.append({"role": "user", "content": user_input})

        # 意图识别
        intent = self._classify_intent(user_input)

        if intent == "plan_trip":
            # 提取信息
            trip_info = self._extract_trip_info(user_input)
            # 生成计划
            plan = self.coordinator.plan_trip(trip_info)
            response = plan["full_report"]

        elif intent == "query_weather":
            destination = self._extract_destination(user_input)
            result = self.coordinator.weather_agent.handle("query", {
                "destination": destination
            })
            response = result["result"]

        else:
            # 通用对话
            response = self._general_chat(user_input)

        # 添加到历史
        self.conversation_history.append({"role": "assistant", "content": response})

        return response

    def _classify_intent(self, text: str) -> str:
        """分类用户意图"""
        if any(word in text for word in ["规划", "行程", "旅行计划"]):
            return "plan_trip"
        elif any(word in text for word in ["天气", "温度", "下雨"]):
            return "query_weather"
        else:
            return "general"

    def _extract_trip_info(self, text: str) -> Dict:
        """提取旅行信息（简化实现）"""
        # 实际应用中应该使用更复杂的NLP或LLM
        return {
            "destination": "北京",  # 默认值
            "duration": 3,
            "dates": "下个月",
            "preferences": "文化历史",
            "people_count": 1
        }

    def _extract_destination(self, text: str) -> str:
        """提取目的地"""
        # 简化实现
        return "北京"

    def _general_chat(self, user_input: str) -> str:
        """通用对话"""
        prompt = f"""
你是一个专业的旅行助手。用户说：{user_input}

请给出友好、专业的回复。
"""

        messages = [{"role": "user", "content": prompt}]
        return self.llm_client.think(messages)


# 使用示例
if __name__ == "__main__":
    chatbot = TravelChatbot()

    # 模拟对话
    conversations = [
        "你好，我想规划一次旅行",
        "我想去杭州玩3天",
        "那边天气怎么样？"
    ]

    for user_msg in conversations:
        print(f"\n用户: {user_msg}")
        response = chatbot.chat(user_msg)
        print(f"助手: {response[:200]}...")
```

---

## 项目总结

### 技术亮点

1. **多智能体协作** - 不同专业智能体分工合作
2. **上下文共享** - 智能体间传递信息
3. **分层架构** - 清晰的模块划分
4. **可扩展性** - 易于添加新功能

### 实现效果

- ✅ 自动化旅行规划
- ✅ 智能推荐系统
- ✅ 预算精准估算
- ✅ 详细行程生成
- ✅ 对话式交互

### 扩展方向

- 🗺️ 集成真实地图API
- 📱 开发移动端应用
- 🌐 支持多语言
- 💾 添加用户偏好学习
- 📊 数据分析和优化

---

## 参考资源

- [LangChain Multi-Agent](https://python.langchain.com/docs/use_cases/agent_simulations)
- [AutoGen Documentation](https://microsoft.github.io/autogen/)
- [旅行规划API](https://partners.skyscanner.net/)

---

## 许可证

MIT License

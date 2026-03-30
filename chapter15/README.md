# 第十五章：构建赛博小镇

> Agent与游戏的结合，模拟社会动态

**本章目标**：
- 理解多智能体模拟原理
- 构建虚拟社会系统
- 观察复杂的社会行为涌现

---

## 项目概述

### 什么是赛博小镇？

**Cyber Town** 是一个由AI智能体组成的虚拟社会，每个智能体都有：
- 👤 独特的性格和记忆
- 💼 不同的职业和技能
- 🤝 社交关系网络
- 🎯 个人目标和动机
- 📅 每日生活轨迹

### 核心概念

```
智能体社会模拟
├── 角色系统 - 职业、性格、背景
├── 关系系统 - 社交网络、情感纽带
├── 行为系统 - 日常活动、决策
├── 事件系统 - 随机事件、突发状况
└── 进化系统 - 学习、成长、变化
```

---

## 系统设计

### 社会结构

```
┌────────────────────────────────────┐
│         赛博小镇生态系统            │
├────────────────────────────────────┤
│                                    │
│  ┌────────┐  ┌────────┐           │
│  │ 居民A  │──│ 居民B  │           │
│  │ 医生   │  │ 教师   │           │
│  └────┬───┘  └────┬───┘           │
│       │           │               │
│       └─────┬─────┘               │
│             │                     │
│      ┌──────▼──────┐             │
│      │   市政厅    │             │
│      │  协调中心   │             │
│      └─────────────┘             │
│                                    │
│  设施：医院、学校、商店、公园      │
│  事件：节日、灾难、选举、市场      │
└────────────────────────────────────┘
```

---

## 实现代码

### 1. 角色系统

```python
# character_system.py

from typing import List, Dict, Optional
from enum import Enum
import random
from datetime import datetime, timedelta


class Profession(Enum):
    """职业类型"""
    DOCTOR = "医生"
    TEACHER = "教师"
    ENGINEER = "工程师"
    ARTIST = "艺术家"
    MERCHANT = "商人"
    FARMER = "农民"


class PersonalityType(Enum):
    """性格类型"""
    EXTROVERT = "外向"
    INTROVERT = "内向"
    AGREEABLE = "友善"
    NEUROTIC = "神经质"
    CONSCIENTIOUS = "尽责"


class Character:
    """角色类 - 表示小镇中的一个智能体"""

    def __init__(self,
                 name: str,
                 age: int,
                 profession: Profession,
                 personality: List[PersonalityType]):
        self.name = name
        self.age = age
        self.profession = profession
        self.personality = personality

        # 基本属性
        self.health = 100
        self.happiness = 80
        self.money = random.randint(1000, 5000)
        self.energy = 100

        # 社交关系
        self.friends = []
        self.enemies = []
        self.family = []

        # 记忆系统
        self.memories = []

        # 当前状态
        self.current_location = "家"
        self.current_activity = "休息"
        self.current_time = datetime.now()

    def introduce(self) -> str:
        """自我介绍"""
        personality_str = "、".join([p.value for p in self.personality])
        return (f"我叫{self.name}，{self.age}岁，"
                f"是一名{self.profession.value}。"
                f"我的性格是{personality_str}。")

    def decide_action(self, context: Dict) -> str:
        """决定下一步行动"""
        hour = self.current_time.hour

        # 根据时间和性格决定行为
        if 6 <= hour < 9:
            return "晨练"
        elif 9 <= hour < 12:
            return self._work_activity()
        elif 12 <= hour < 14:
            return "午餐"
        elif 14 <= hour < 18:
            return self._work_activity()
        elif 18 <= hour < 22:
            if PersonalityType.EXTROVERT in self.personality:
                return "社交"
            else:
                return "在家休息"
        else:
            return "睡觉"

    def _work_activity(self) -> str:
        """工作相关活动"""
        activities = {
            Profession.DOCTOR: ["诊断病人", "做手术", "写病历"],
            Profession.TEACHER: ["上课", "批改作业", "备课"],
            Profession.ENGINEER: ["设计", "调试", "开会"],
            Profession.ARTIST: ["创作", "找灵感", "展览"],
            Profession.MERCHANT: ["进货", "销售", "记账"],
            Profession.FARMER: ["种植", "收割", "卖农产品"]
        }
        return random.choice(activities[self.profession])

    def interact(self, other: 'Character') -> str:
        """与其他角色互动"""
        if other in self.friends:
            return f"{self.name}和{other.name}愉快地聊天"
        elif other in self.enemies:
            return f"{self.name}和{other.name}发生了争执"
        else:
            # 根据性格决定是否建立新关系
            if PersonalityType.AGREEABLE in self.personality and random.random() > 0.5:
                self.friends.append(other)
                return f"{self.name}主动和{other.name}打招呼，他们成为了朋友"
            else:
                return f"{self.name}和{other.name}礼貌地点头致意"

    def add_memory(self, memory: str):
        """添加记忆"""
        self.memories.append({
            "time": datetime.now(),
            "content": memory
        })

    def reflect(self) -> str:
        """回顾一天"""
        recent_memories = self.memories[-5:] if len(self.memories) >= 5 else self.memories
        return f"{self.name}回忆道：{[m['content'] for m in recent_memories]}"


class CharacterFactory:
    """角色工厂 - 用于生成角色"""

    @staticmethod
    def create_random_character(name: str) -> Character:
        """创建随机角色"""
        age = random.randint(18, 65)
        profession = random.choice(list(Profession))

        # 随机性格组合
        num_traits = random.randint(2, 3)
        personality = random.sample(list(PersonalityType), num_traits)

        return Character(name, age, profession, personality)

    @staticmethod
    def create_family(surname: str, size: int = 3) -> List[Character]:
        """创建一个家庭"""
        family = []

        # 父母
        father = CharacterFactory.create_random_character(f"{surname}先生")
        father.age = random.randint(35, 55)

        mother = CharacterFactory.create_random_character(f"{surname}太太")
        mother.age = random.randint(30, 50)

        family.extend([father, mother])

        # 孩子
        for i in range(size - 2):
            child = CharacterFactory.create_random_character(f"{surname}家{i+1}号孩子")
            child.age = random.randint(5, 18)
            family.append(child)

        # 建立家庭关系
        for member in family:
            member.family = [m for m in family if m != member]

        return family
```

### 2. 小镇系统

```python
# town_system.py

from typing import List, Dict
from character_system import Character, CharacterFactory, Profession
import random


class Town:
    """小镇类 - 管理所有居民和设施"""

    def __init__(self, name: str):
        self.name = name
        self.residents: List[Character] = []
        self.locations = {
            "医院": {"type": "工作场所", "capacity": 10},
            "学校": {"type": "工作场所", "capacity": 15},
            "工厂": {"type": "工作场所", "capacity": 20},
            "商店": {"type": "服务场所", "capacity": 5},
            "公园": {"type": "休闲场所", "capacity": 50},
            "餐厅": {"type": "服务场所", "capacity": 20}
        }
        self.time = 0  # 游戏时间（小时）
        self.events = []

    def add_resident(self, character: Character):
        """添加居民"""
        self.residents.append(character)
        print(f"✓ {character.name} 搬到了 {self.name}")

    def initialize_population(self, size: int = 20):
        """初始化人口"""
        print(f"\n初始化 {self.name} 的人口...")

        # 创建几个家庭
        surnames = ["张", "李", "王", "赵", "陈"]
        for surname in surnames[:size//4]:
            family = CharacterFactory.create_family(surname, random.randint(3, 5))
            for member in family:
                self.add_resident(member)

        # 添加一些单身居民
        for i in range(size - len(self.residents)):
            resident = CharacterFactory.create_random_character(f"居民{i+1}号")
            self.add_resident(resident)

        print(f"✓ {self.name} 现在有 {len(self.residents)} 位居民\n")

    def simulate_hour(self):
        """模拟一小时"""
        self.time += 1
        hour = self.time % 24

        print(f"\n🕐 时间: {hour:02d}:00")

        # 每个角色决定行动
        for resident in self.residents:
            resident.current_time = resident.current_time.replace(hour=hour)
            action = resident.decide_action({"hour": hour})
            resident.current_activity = action

            # 更新状态
            self._update_character_state(resident, action)

        # 处理随机事件
        if random.random() < 0.1:  # 10%概率发生事件
            self._trigger_random_event()

    def _update_character_state(self, character: Character, action: str):
        """更新角色状态"""
        if action == "睡觉":
            character.energy = min(100, character.energy + 10)
            character.health = min(100, character.health + 1)
        elif action in ["工作活动", "诊断病人", "上课"]:
            character.energy -= 10
            character.money += random.randint(10, 50)
        elif action == "社交":
            character.happiness = min(100, character.happiness + 5)

    def _trigger_random_event(self):
        """触发随机事件"""
        events = [
            "节日庆典，所有人快乐度+10",
            "流行感冒，所有人健康度-5",
            "彩票开奖，有人发财了",
            "暴雨，大家只能待在家里"
        ]

        event = random.choice(events)
        print(f"\n📢 事件: {event}")

        self.events.append({
            "time": self.time,
            "description": event
        })

        # 事件影响
        if "节日" in event:
            for resident in self.residents:
                resident.happiness = min(100, resident.happiness + 10)
        elif "感冒" in event:
            for resident in self.residents:
                resident.health -= 5

    def simulate_day(self) -> Dict:
        """模拟一天"""
        print(f"\n{'='*50}")
        print(f"📅 {self.name} 的新一天")
        print(f"{'='*50}")

        # 模拟24小时
        for _ in range(24):
            self.simulate_hour()

        # 生成日报
        return self.generate_daily_report()

    def generate_daily_report(self) -> Dict:
        """生成每日报告"""
        avg_happiness = sum(r.happiness for r in self.residents) / len(self.residents)
        avg_health = sum(r.health for r in self.residents) / len(self.residents)
        total_money = sum(r.money for r in self.residents)

        report = {
            "day": self.time // 24,
            "population": len(self.residents),
            "avg_happiness": avg_happiness,
            "avg_health": avg_health,
            "total_money": total_money,
            "events_today": len([e for e in self.events if e["time"] // 24 == self.time // 24])
        }

        print(f"\n{'='*50}")
        print("📊 每日统计")
        print(f"{'='*50}")
        print(f"人口: {report['population']}")
        print(f"平均快乐度: {report['avg_happiness']:.1f}")
        print(f"平均健康度: {report['avg_health']:.1f}")
        print(f"总财富: ${report['total_money']}")
        print(f"今日事件: {report['events_today']} 个")

        return report

    def get_social_network(self) -> Dict[str, List[str]]:
        """获取社交网络"""
        network = {}
        for resident in self.residents:
            friends = [f.name for f in resident.friends]
            network[resident.name] = friends
        return network
```

### 3. 社会互动系统

```python
# social_system.py

from typing import List, Dict
from character_system import Character
import random


class SocialSystem:
    """社会系统 - 处理角色间的互动"""

    def __init__(self):
        self.relationships = {}
        self.interactions = []

    def facilitate_interaction(self, char1: Character, char2: Character) -> str:
        """促进两个角色之间的互动"""
        interaction = char1.interact(char2)

        self.interactions.append({
            "participants": [char1.name, char2.name],
            "type": "社交",
            "description": interaction
        })

        return interaction

    def organize_community_event(self, town_residents: List[Character]) -> List[str]:
        """组织社区活动"""
        event_types = [
            "节日庆典",
            "市集",
            "才艺表演",
            "体育比赛",
            "慈善晚会"
        ]

        event = random.choice(event_types)
        results = []

        print(f"\n🎉 {self.name}举办{event}！")

        # 随机选择参与者
        participants = random.sample(town_residents, min(10, len(town_residents)))

        for participant in participants:
            # 参与活动提升快乐度
            participant.happiness = min(100, participant.happiness + 15)

            # 可能建立新友谊
            if random.random() > 0.7:
                others = [p for p in participants if p != participant]
                if others:
                    new_friend = random.choice(others)
                    if new_friend not in participant.friends:
                        participant.friends.append(new_friend)
                        results.append(f"{participant.name}和{new_friend.name}成为了朋友")

        return results

    def simulate_gossip(self, town_residents: List[Character]) -> None:
        """模拟流言传播"""
        # 随机选择一个话题
        gossips = [
            "有人在市集上捡到了金币",
            "医生研制出了新药",
            "有外地商人要来投资",
            "今年会是丰收年"
        ]

        gossip = random.choice(gossips)

        # 从一个人开始传播
        starter = random.choice(town_residents)
        spreaders = [starter]

        print(f"\n💬 流言传播: {gossip}")
        print(f"  起源: {starter.name}")

        # 传播3轮
        for round_num in range(3):
            new_spreaders = []

            for spreader in spreaders:
                # 传播给朋友
                friends = spreader.friends
                if friends and random.random() > 0.3:
                    recipient = random.choice(friends)
                    if recipient not in spreaders:
                        new_spreaders.append(recipient)
                        print(f"  第{round_num+1}轮: {spreader.name}告诉了{recipient.name}")

            spreaders.extend(new_spreaders)

            if not new_spreaders:
                break
```

### 4. 主程序

```python
# cyber_town_main.py

from town_system import Town
from social_system import SocialSystem
import time


def main():
    """主程序"""
    print("\n" + "="*50)
    print("🏘️  赛博小镇模拟器")
    print("="*50)

    # 创建小镇
    town = Town("幸福镇")

    # 初始化人口
    town.initialize_population(size=20)

    # 创建社会系统
    social_system = SocialSystem()

    # 介绍几位居民
    print("\n👥 部分居民介绍：")
    for resident in town.residents[:5]:
        print(f"  - {resident.introduce()}")

    # 模拟运行
    print("\n开始模拟...")
    print("="*50)

    try:
        # 模拟7天
        for day in range(1, 8):
            daily_report = town.simulate_day()

            # 每两天组织一次社区活动
            if day % 2 == 0:
                results = social_system.organize_community_event(town.residents)
                for result in results:
                    print(f"  {result}")

            # 模拟流言传播
            if day == 4:
                social_system.simulate_gossip(town.residents)

            # 暂停一下让用户看清
            time.sleep(1)

    except KeyboardInterrupt:
        print("\n\n⏸️  模拟已暂停")

    # 最终统计
    print("\n" + "="*50)
    print("📊 最终统计")
    print("="*50)

    happiest = max(town.residents, key=lambda r: r.happiness)
    richest = max(town.residents, key=lambda r: r.money)

    print(f"最快乐的居民: {happiest.name} (快乐度: {happiest.happiness})")
    print(f"最富有的居民: {richest.name} (财富: ${richest.money})")

    # 社交网络统计
    total_friendships = sum(len(r.friends) for r in town.residents)
    print(f"总友谊数: {total_friendships}")
    print(f"平均每人朋友数: {total_friendships/len(town.residents):.1f}")


if __name__ == "__main__":
    main()
```

---

## 项目扩展

### 添加经济系统

```python
# economy_system.py

class EconomySystem:
    """经济系统"""

    def __init__(self):
        self.prices = {}
        self.market_trends = []

    def update_prices(self):
        """更新物价"""
        # 根据供需关系调整价格
        pass

    def facilitate_trade(self, char1: Character, char2: Character):
        """促进交易"""
        pass
```

### 添加政治系统

```python
# political_system.py

class PoliticalSystem:
    """政治系统"""

    def __init__(self, town: Town):
        self.town = town
        self.mayor = None
        self.policies = []

    def hold_election(self):
        """举行选举"""
        pass

    def propose_policy(self, policy: str):
        """提出政策"""
        pass
```

---

## 项目总结

### 技术亮点

1. **复杂系统建模** - 多层次的社会结构
2. **智能体行为** - 个性化决策机制
3. **社交网络** - 动态关系演化
4. **事件系统** - 随机性与叙事性

### 观察到的现象

- 🔄 社交网络的自发形成
- 📈 财富的不平等分布
- 😊 快乐度的传染效应
- 🎭 个性对行为的影响

### 学习价值

- 理解社会动力学
- 实践多智能体编程
- 观察复杂系统涌现
- 探索人机交互

---

## 参考资源

- [Generative Agents](https://arxiv.org/abs/2304.03442)
- [Smallville](https://github.com/joonspk-research/generative_agents)
- [Minecraft Simulation](https://www.youtube.com/watch?v=vGQqLmypaQY)

---

## 许可证

MIT License

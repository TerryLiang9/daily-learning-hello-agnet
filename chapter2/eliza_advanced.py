"""
增强版ELIZA聊天机器人
====================

基于1966年Joseph Weizenbaum的经典ELIZA程序,添加以下增强功能:
1. 扩展的规则库(覆盖工作、学习、爱好等话题)
2. 上下文记忆系统(记住用户姓名、年龄、职业等信息)
3. 对话历史记录
4. 置信度评分

作者: DataWhale Hello-Agents学习项目
"""

import re
import random
from typing import Dict, List, Tuple, Optional
from collections import deque


class ConversationMemory:
    """对话记忆系统"""

    def __init__(self, max_history: int = 10):
        self.user_profile: Dict[str, str] = {}  # 用户画像
        self.conversation_history: deque = deque(maxlen=max_history)  # 对话历史
        self.turn_count = 0  # 对话轮次

    def remember_fact(self, key: str, value: str):
        """记住用户信息"""
        self.user_profile[key] = value
        print(f"[记忆: 已记住你的{key}是{value}]")

    def recall_fact(self, key: str) -> Optional[str]:
        """回忆用户信息"""
        return self.user_profile.get(key)

    def add_to_history(self, user_input: str, bot_response: str):
        """添加到对话历史"""
        self.turn_count += 1
        self.conversation_history.append({
            'turn': self.turn_count,
            'user': user_input,
            'bot': bot_response
        })

    def has_context(self) -> bool:
        """是否有上下文信息"""
        return len(self.user_profile) > 0


class ElizaAdvanced:
    """增强版ELIZA聊天机器人"""

    def __init__(self):
        self.memory = ConversationMemory()

        # 代词转换规则
        self.pronoun_swap = {
            "i": "you", "you": "i", "me": "you", "my": "your",
            "am": "are", "are": "am", "was": "were", "i'd": "you would",
            "i've": "you have", "i'll": "you will", "yours": "mine",
            "mine": "yours", "yourself": "myself", "myself": "yourself"
        }

        # 规则库: (优先级, 模式, 响应模板列表)
        # 优先级数字越大越优先匹配
        self.rules = [
            # 高优先级: 用户信息提取
            (100, r'my name is (.*)', [
                ("name", "{0}", "Nice to meet you, {0}. How can I help you today?")
            ]),
            (100, r'i am (.*) years old', [
                ("age", "{0}", "{0} is a great age. What do you like to do?")
            ]),
            (100, r'i work as (an? )?(.*)', [
                ("job", "{1}", "Being a {1} sounds interesting. What do you like about it?")
            ]),
            (100, r'i am a (.*)', [
                ("job", "{0}", "Being a {0} sounds interesting. Tell me more about it.")
            ]),

            # 中优先级: 工作相关
            (80, r'i (work|job) .* (company|office)', [
                (None, "Tell me more about your work environment."),
                (None, "How do you feel about your workplace?")
            ]),
            (80, r'my (boss|manager|colleague) (.*)', [
                (None, "How does that make you feel about your work?"),
                (None, "Tell me more about this relationship.")
            ]),
            (80, r'i (don\'t|do not) like my job', [
                (None, "What aspects of your job do you find difficult?"),
                (None, "Is there a particular reason you feel this way?")
            ]),

            # 中优先级: 学习相关
            (80, r'i am studying (.*)', [
                ("subject", "{0}", "{0} is a fascinating subject. What interests you most about it?"),
                (None, "Tell me more about your studies.")
            ]),
            (80, r'i (want to|would like to) learn (.*)', [
                ("subject", "{1}", "Learning {1} is a great goal. What motivated this interest?"),
                (None, "That's a good skill to develop.")
            ]),
            (80, r'i (study|learn) .* (school|university|college)', [
                (None, "How is your educational experience going?"),
                (None, "Tell me about your studies.")
            ]),

            # 中优先级: 爱好相关
            (80, r'i like (.*)', [
                ("hobby", "{0}", "Tell me more about why you enjoy {0}."),
                (None, "That sounds interesting. How did you get into that?")
            ]),
            (80, r'i love (to )?(.*)', [
                ("hobby", "{1}", "What do you love most about it?"),
                (None, "Tell me more about your passion for this.")
            ]),
            (80, r'my hobby is (.*)', [
                ("hobby", "{0}", "{0} is a wonderful hobby. How often do you do it?"),
            ]),
            (80, r'i (play|watch) (.*)', [
                ("hobby", "{1}", "Do you find it relaxing or exciting?"),
            ]),

            # 中优先级: 情感表达
            (70, r'i feel (.*)', [
                (None, "Why do you feel {0}?"),
                (None, "Tell me more about feeling {0}.")
            ]),
            (70, r'i am (happy|sad|angry|excited|worried)', [
                (None, "What makes you feel {1}?"),
                (None, "How long have you been feeling {1}?")
            ]),
            (70, r'i (.*) (stressed|anxious|depressed)', [
                (None, "What's causing you to feel {2}?"),
                (None, "Tell me more about these feelings.")
            ]),

            # 基础规则(继承自原始ELIZA)
            (60, r'I need (.*)', [
                (None, "Why do you need {0}?"),
                (None, "Would it really help you to get {0}?"),
                (None, "Are you sure you need {0}?")
            ]),
            (60, r'Why don\'t you (.*)', [
                (None, "Do you really think I don't {0}?"),
                (None, "Perhaps eventually I will {0}."),
                (None, "Do you really want me to {0}?")
            ]),
            (60, r'Why can\'t I (.*)', [
                (None, "Do you think you should be able to {0}?"),
                (None, "If you could {0}, what would you do?"),
                (None, "I don't know -- why can't you {0}?")
            ]),
            (60, r'I can\'t (.*)', [
                (None, "How do you know you can't {0}?"),
                (None, "Perhaps you could {0} if you tried."),
                (None, "What would it take for you to {0}?")
            ]),
            (60, r'I am (.*)', [
                (None, "How long have you been {0}?"),
                (None, "How do you feel about being {0}?"),
                (None, "Did you come to me because you are {0}?")
            ]),
            (50, r'.* mother .*', [
                (None, "Tell me more about your mother."),
                (None, "How do you feel about your mother?"),
                (None, "What was your relationship with your mother like?")
            ]),
            (50, r'.* father .*', [
                (None, "Tell me more about your father."),
                (None, "How did your father make you feel?"),
                (None, "What has your father taught you?")
            ]),

            # 上下文相关:如果已知道用户信息
            (40, r'what do you (know|think) about me', [
                (None, "CONTEXT_AWARE"),
                (None, "I remember some things about you.")
            ]),
            (40, r'(do you )?remember me', [
                (None, "CONTEXT_AWARE"),
                (None, "I remember talking with you.")
            ]),
        ]

        # 默认回复(当没有匹配规则时)
        self.default_responses = [
            "Please tell me more.",
            "Let's change focus a bit... Tell me about your family.",
            "Can you elaborate on that?",
            "Why do you say that?",
            "I see. Tell me more.",
            "How does that make you feel?",
            "Interesting. Please continue."
        ]

    def swap_pronouns(self, phrase: str) -> str:
        """代词转换"""
        words = phrase.lower().split()
        swapped_words = [self.pronoun_swap.get(word, word) for word in words]
        return " ".join(swapped_words)

    def extract_and_remember(self, pattern: str, match: re.Match) -> Optional[Tuple]:
        """从匹配中提取并记住用户信息"""
        for rule in self.rules:
            if pattern in rule[1]:
                for response in rule[2]:
                    if isinstance(response, tuple) and response[0]:
                        key, value_template, _ = response
                        if key:
                            # 提取值
                            try:
                                value = match.group(1) if match.groups() else ""
                                value = value.strip()
                                if value:
                                    self.memory.remember_fact(key, value)
                            except IndexError:
                                pass
        return None

    def generate_context_aware_response(self, user_input: str) -> Optional[str]:
        """生成基于上下文的回复"""
        if not self.memory.has_context():
            return None

        # 如果用户问"你知道关于我什么"
        if re.search(r'what do you (know|think) about me', user_input, re.IGNORECASE):
            if self.memory.user_profile:
                facts = ", ".join([f"{k}: {v}" for k, v in self.memory.user_profile.items()])
                return f"I remember that {facts}. Is there anything else you'd like to share?"
            else:
                return "I'd like to know more about you. Can you tell me about yourself?"

        # 如果用户问"记得我吗"
        if re.search(r'(do you )?remember me', user_input, re.IGNORECASE):
            turn_info = f"we've talked for {self.memory.turn_count} turns"
            if self.memory.user_profile:
                facts = ", ".join([f"you're {v}" for v in self.memory.user_profile.values()])
                return f"Yes, I remember you! {facts}, and {turn_info}. How are you today?"
            else:
                return f"Yes, I remember our conversation. We've had {self.memory.turn_count} turns. How are you?"

        # 如果用户提到家人,且知道职业
        if re.search(r'.* (mother|father|parent) .*', user_input, re.IGNORECASE):
            job = self.memory.recall_fact('job')
            if job:
                return f"How do your parents feel about you being a {job}?"

        return None

    def respond(self, user_input: str) -> Tuple[str, float]:
        """
        生成回复
        返回: (回复文本, 置信度分数)
        """
        # 首先检查是否有上下文相关的回复
        context_response = self.generate_context_aware_response(user_input)
        if context_response:
            self.memory.add_to_history(user_input, context_response)
            return context_response, 0.9

        # 按优先级排序规则
        sorted_rules = sorted(self.rules, key=lambda x: x[0], reverse=True)

        # 尝试匹配规则
        for priority, pattern, responses in sorted_rules:
            match = re.search(pattern, user_input, re.IGNORECASE)
            if match:
                # 提取并记住用户信息
                self.extract_and_remember(pattern, match)

                # 随机选择一个响应模板
                response_data = random.choice(responses)

                if isinstance(response_data, tuple):
                    key, value_template, response_template = response_data

                    if response_template == "CONTEXT_AWARE":
                        # 这个规则已经被上下文处理器处理了
                        continue

                    # 捕获匹配到的部分
                    captured = match.group(1) if match.groups() else ''
                    # 进行代词转换
                    captured_swapped = self.swap_pronouns(captured)
                    # 格式化响应
                    response = response_template.format(captured_swapped)
                else:
                    # 旧格式兼容
                    captured = match.group(1) if match.groups() else ''
                    captured_swapped = self.swap_pronouns(captured)
                    response = response_data.format(captured_swapped)

                self.memory.add_to_history(user_input, response)
                return response, priority / 100.0

        # 如果没有匹配任何特定规则,使用默认回复
        default_response = random.choice(self.default_responses)
        self.memory.add_to_history(user_input, default_response)
        return default_response, 0.1

    def show_memory(self):
        """显示记忆内容"""
        if self.memory.user_profile:
            print("\n[用户画像]")
            for key, value in self.memory.user_profile.items():
                print(f"  {key}: {value}")

        if self.memory.conversation_history:
            print(f"\n[对话历史: 最近{min(3, len(self.memory.conversation_history))}轮]")
            for turn in list(self.memory.conversation_history)[-3:]:
                print(f"  第{turn['turn']}轮")
                print(f"    用户: {turn['user']}")
                print(f"    机器人: {turn['bot']}")


def main():
    """主对话循环"""
    print("=" * 60)
    print("增强版ELIZA聊天机器人")
    print("=" * 60)
    print("基于1966年Joseph Weizenbaum的经典程序,增强了上下文记忆功能")
    print("\n你可以:")
    print("  - 告诉我你的名字、年龄、职业")
    print("  - 谈论你的工作、学习、爱好")
    print("  - 分享你的感受")
    print("  - 输入 'memory' 查看我记住了什么")
    print("  - 输入 'quit', 'exit', 'bye' 退出")
    print("=" * 60)
    print()

    eliza = ElizaAdvanced()
    print("Eliza: 你好!我是Eliza,一个心理咨询机器人。今天想聊点什么?\n")

    while True:
        try:
            user_input = input("You: ").strip()

            if not user_input:
                continue

            if user_input.lower() in ["quit", "exit", "bye"]:
                print("Eliza: 再见!很高兴和你聊天。祝你有美好的一天! 👋")
                break

            if user_input.lower() == "memory":
                eliza.show_memory()
                print()
                continue

            response, confidence = eliza.respond(user_input)
            print(f"Eliza: {response}")

        except KeyboardInterrupt:
            print("\n\nEliza: 看来你需要离开了。再见! 👋")
            break
        except Exception as e:
            print(f"Eliza: 抱歉,我遇到了一些问题。请继续...\n")


if __name__ == '__main__':
    main()

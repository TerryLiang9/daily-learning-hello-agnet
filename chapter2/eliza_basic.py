"""
基础版ELIZA聊天机器人
====================

基于1966年Joseph Weizenbaum的经典ELIZA程序的简化实现。
展示了符号主义AI的核心思想:基于规则的模式匹配与文本替换。

核心算法:
1. 关键词识别与优先级排序
2. 分解模式(使用正则表达式和通配符捕获)
3. 重组模式(模板填充)
4. 代词转换(I ↔ you, my ↔ your等)

作者: DataWhale Hello-Agents学习项目
"""

import re
import random


def swap_pronouns(phrase):
    """
    代词转换
    将第一人称代词转换为第二人称,以维持对话连贯性
    """
    pronoun_map = {
        "i": "you", "you": "i", "me": "you", "my": "your",
        "am": "are", "are": "am", "was": "were", "i'd": "you would",
        "i've": "you have", "i'll": "you will", "yours": "mine",
        "mine": "yours"
    }
    words = phrase.lower().split()
    swapped_words = [pronoun_map.get(word, word) for word in words]
    return " ".join(swapped_words)


def respond(user_input):
    """
    生成响应
    基于模式匹配和规则库生成回复
    """
    # 规则库:模式(正则表达式) -> 响应模板列表
    rules = {
        # 高优先级: 特定句式
        r'I need (.*)': [
            "Why do you need {0}?",
            "Would it really help you to get {0}?",
            "Are you sure you need {0}?"
        ],
        r'Why don\'t you (.*)\?': [
            "Do you really think I don't {0}?",
            "Perhaps eventually I will {0}.",
            "Do you really want me to {0}?"
        ],
        r'Why can\'t I (.*)\?': [
            "Do you think you should be able to {0}?",
            "If you could {0}, what would you do?",
            "I don't know -- why can't you {0}?"
        ],
        r'I can\'t (.*)': [
            "How do you know you can't {0}?",
            "Perhaps you could {0} if you tried.",
            "What would it take for you to {0}?"
        ],
        r'I am (.*)': [
            "How long have you been {0}?",
            "How do you feel about being {0}?",
            "Did you come to me because you are {0}?",
            "Tell me more about being {0}."
        ],

        # 中优先级: 家庭相关
        r'.* mother .*': [
            "Tell me more about your mother.",
            "What was your relationship with your mother like?",
            "How do you feel about your mother?",
            "How does your mother make you feel?"
        ],
        r'.* father .*': [
            "Tell me more about your father.",
            "How did your father make you feel?",
            "What has your father taught you?",
            "How do you feel about your father?"
        ],
        r'.* family .*': [
            "Tell me more about your family.",
            "How is your relationship with your family?",
        ],

        # 中优先级: 情感相关
        r'I feel (.*)': [
            "Why do you feel {0}?",
            "Tell me more about feeling {0}.",
            "Do you often feel {0}?",
        ],
        r'I am (.*) (happy|sad|angry|excited)': [
            "What makes you feel {2}?",
            "How long have you been feeling {2}?",
        ],

        # 低优先级: 疑问句
        r'(.*)\?': [
            "Why do you ask that?",
            "Please tell me more.",
            "What do you think?",
        ],

        # 默认规则(最低优先级)
        r'.*': [
            "Please tell me more.",
            "Let's change focus a bit... Tell me about your family.",
            "Can you elaborate on that?",
            "Why do you say that?",
            "I see. Tell me more.",
            "How does that make you feel?",
        ]
    }

    # 按顺序尝试匹配规则
    for pattern, responses in rules.items():
        match = re.search(pattern, user_input, re.IGNORECASE)
        if match:
            # 捕获匹配到的部分
            captured_group = match.group(1) if match.groups() else ''

            # 进行代词转换
            swapped_group = swap_pronouns(captured_group)

            # 从模板中随机选择一个并格式化
            response = random.choice(responses).format(swapped_group)
            return response

    # 理论上不会到这里,因为最后的 r'.*' 规则会匹配所有输入
    return "Please tell me more."


def main():
    """主对话循环"""
    print("=" * 60)
    print("ELIZA - 心理咨询聊天机器人")
    print("=" * 60)
    print("基于1966年MIT的Joseph Weizenbaum开发的经典程序")
    print("\n输入 'quit', 'exit', 或 'bye' 退出")
    print("=" * 60)
    print()

    print("Eliza: 你好!我是Eliza。今天有什么想聊的吗?\n")

    while True:
        try:
            user_input = input("You: ").strip()

            if not user_input:
                continue

            if user_input.lower() in ["quit", "exit", "bye"]:
                print("Eliza: 再见!很高兴和你聊天。👋")
                break

            response = respond(user_input)
            print(f"Eliza: {response}\n")

        except KeyboardInterrupt:
            print("\n\nEliza: 再见! 👋")
            break
        except Exception as e:
            print(f"Eliza: 抱歉,我遇到了一些问题。请继续...\n")


if __name__ == '__main__':
    main()

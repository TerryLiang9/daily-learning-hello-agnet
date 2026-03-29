"""
N-gram语言模型演示
==================

展示统计语言模型的基本原理:
1. 马尔可夫假设
2. 最大似然估计
3. Bigram/Trigram概率计算
4. N-gram模型的局限性

作者: DataWhale Hello-Agents学习项目
"""

import collections
import re
import sys
import io
from typing import List, Tuple, Dict

# 修复 Windows 终端编码问题
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


class NGramModel:
    """N-gram语言模型"""

    def __init__(self, n: int = 2):
        """
        初始化N-gram模型
        Args:
            n: n-gram的阶数(2=bigram, 3=trigram)
        """
        self.n = n
        self.unigram_counts: Dict[str, int] = collections.defaultdict(int)
        self.ngram_counts: Dict[Tuple, int] = collections.defaultdict(int)
        self.context_counts: Dict[Tuple, int] = collections.defaultdict(int)
        self.total_tokens = 0
        self.vocabulary = set()

    def train(self, corpus: str):
        """
        训练模型
        Args:
            corpus: 训练语料(字符串)
        """
        # 分词
        tokens = self._tokenize(corpus)
        self.total_tokens = len(tokens)
        self.vocabulary = set(tokens)

        # 统计unigram
        for token in tokens:
            self.unigram_counts[token] += 1

        # 统计n-gram和上下文
        for i in range(len(tokens) - self.n + 1):
            ngram = tuple(tokens[i:i + self.n])
            context = tuple(tokens[i:i + self.n - 1])

            self.ngram_counts[ngram] += 1
            self.context_counts[context] += 1

        print(f"训练完成!")
        print(f"  词表大小: {len(self.vocabulary)}")
        print(f"  总Token数: {self.total_tokens}")
        print(f"  唯一{self.n}-gram数: {len(self.ngram_counts)}")

    def _tokenize(self, text: str) -> List[str]:
        """简单的分词器"""
        # 转小写,按空格分词
        tokens = text.lower().split()
        return tokens

    def unigram_probability(self, word: str) -> float:
        """计算unigram概率 P(word)"""
        if self.total_tokens == 0:
            return 0.0
        return self.unigram_counts.get(word, 0) / self.total_tokens

    def ngram_probability(self, ngram: Tuple[str, ...]) -> float:
        """
        计算n-gram概率 P(w_n | w_1, ..., w_{n-1})
        使用最大似然估计: Count(w_1, ..., w_n) / Count(w_1, ..., w_{n-1})
        """
        if len(ngram) != self.n:
            raise ValueError(f"Expected {self.n}-gram, got {len(ngram)}-gram")

        context = ngram[:-1]
        ngram_count = self.ngram_counts.get(ngram, 0)
        context_count = self.context_counts.get(context, 0)

        if context_count == 0:
            return 0.0

        return ngram_count / context_count

    def sentence_probability(self, sentence: str) -> float:
        """
        计算句子概率 P(sentence)
        根据链式法则和马尔可夫假设
        """
        tokens = self._tokenize(sentence)

        if len(tokens) < self.n:
            # 如果句子太短,使用unigram
            prob = 1.0
            for token in tokens:
                prob *= self.unigram_probability(token)
            return prob

        # 计算联合概率
        prob = 1.0

        # 第一个词:使用unigram
        prob *= self.unigram_probability(tokens[0])

        # 后续词:使用n-gram
        for i in range(1, len(tokens)):
            if i < self.n - 1:
                # 前n-1个词,使用unigram作为近似
                prob *= self.unigram_probability(tokens[i])
            else:
                # 构建n-gram
                ngram = tuple(tokens[max(0, i - self.n + 1):i + 1])
                prob *= self.ngram_probability(ngram)

            # 如果概率为0,提前终止
            if prob == 0:
                break

        return prob

    def generate_next_token(self, context: List[str], top_k: int = 3) -> List[Tuple[str, float]]:
        """
        给定上下文,预测下一个最可能的token
        Args:
            context: 上下文token列表
            top_k: 返回前k个最可能的token
        Returns:
            [(token, probability), ...] 按概率降序排列
        """
        if len(context) < self.n - 1:
            # 上下文不足,使用unigram
            candidates = [(word, count / self.total_tokens)
                         for word, count in self.unigram_counts.most_common(top_k)]
            return candidates

        # 构建上下文n-1 gram
        context_tuple = tuple(context[-(self.n - 1):])

        # 找到所有以该上下文开头的n-gram
        candidates = []
        context_count = self.context_counts.get(context_tuple, 0)

        if context_count == 0:
            # 上下文未见过,回退到unigram
            candidates = [(word, count / self.total_tokens)
                         for word, count in self.unigram_counts.most_common(top_k)]
            return candidates

        # 计算每个可能的下一个词的概率
        for word in self.vocabulary:
            ngram = context_tuple + (word,)
            ngram_count = self.ngram_counts.get(ngram, 0)
            if ngram_count > 0:
                prob = ngram_count / context_count
                candidates.append((word, prob))

        # 按概率降序排序
        candidates.sort(key=lambda x: x[1], reverse=True)
        return candidates[:top_k]


def demonstrate_bigram():
    """演示Bigram模型"""
    print("=" * 60)
    print("Bigram语言模型演示")
    print("=" * 60)
    print()

    # 创建迷你语料库
    corpus = "datawhale agent learns datawhale agent works"
    print(f"训练语料: {corpus}\n")

    # 训练Bigram模型
    model = NGramModel(n=2)
    model.train(corpus)
    print()

    # 示例1: 计算句子概率
    print("【示例1:计算句子概率】")
    test_sentence = "datawhale agent learns"
    print(f"句子: '{test_sentence}'")

    # 手动计算步骤
    tokens = model._tokenize(test_sentence)
    print(f"\n分步计算:")

    # P(datawhale)
    p_datawhale = model.unigram_probability('datawhale')
    print(f"  P(datawhale) = {model.unigram_counts['datawhale']}/{model.total_tokens} = {p_datawhale:.3f}")

    # P(agent | datawhale)
    p_agent_given_datawhale = model.ngram_probability(('datawhale', 'agent'))
    count_datawhale_agent = model.ngram_counts.get(('datawhale', 'agent'), 0)
    count_datawhale = model.unigram_counts['datawhale']
    print(f"  P(agent|datawhale) = {count_datawhale_agent}/{count_datawhale} = {p_agent_given_datawhale:.3f}")

    # P(learns | agent)
    p_learns_given_agent = model.ngram_probability(('agent', 'learns'))
    count_agent_learns = model.ngram_counts.get(('agent', 'learns'), 0)
    count_agent = model.unigram_counts['agent']
    print(f"  P(learns|agent) = {count_agent_learns}/{count_agent} = {p_learns_given_agent:.3f}")

    # 总概率
    total_prob = model.sentence_probability(test_sentence)
    print(f"\n  P('{test_sentence}') ≈ {p_datawhale:.3f} × {p_agent_given_datawhale:.3f} × {p_learns_given_agent:.3f} = {total_prob:.3f}")
    print()

    # 示例2: 对比不同句子
    print("【示例2:句子概率对比】")
    sentences = [
        "datawhale agent learns",
        "datawhale agent works",
        "agent learns datawhale",  # 词序不同
        "datawhale learns agent"   # 不合理的句子
    ]

    print("句子概率排序:")
    for sent in sentences:
        prob = model.sentence_probability(sent)
        print(f"  P('{sent}') = {prob:.6f}")
    print()

    # 示例3: 预测下一个词
    print("【示例3:预测下一个词】")
    context = ["datawhale", "agent"]
    print(f"给定上下文: {' '.join(context)}")
    predictions = model.generate_next_token(context, top_k=5)
    print("下一个最可能的词:")
    for word, prob in predictions:
        bar = "█" * int(prob * 50)
        print(f"  {word:10s} {prob:.3f} {bar}")
    print()


def demonstrate_trigram():
    """演示Trigram模型"""
    print("=" * 60)
    print("Trigram语言模型演示")
    print("=" * 60)
    print()

    # 更大的语料库
    corpus = "the cat sat on the mat the dog sat on the mat the cat sat on the couch"
    print(f"训练语料: {corpus}\n")

    # 训练Trigram模型
    model = NGramModel(n=3)
    model.train(corpus)
    print()

    # 计算句子概率
    test_sentence = "the cat sat on the mat"
    print(f"句子: '{test_sentence}'")
    prob = model.sentence_probability(test_sentence)
    print(f"P('{test_sentence}') = {prob:.6f}")
    print()

    # 预测下一个词
    context = ["the", "cat", "sat"]
    print(f"给定上下文: {' '.join(context)}")
    predictions = model.generate_next_token(context, top_k=5)
    print("下一个最可能的词:")
    for word, prob in predictions:
        print(f"  {word:10s} {prob:.3f}")
    print()


def demonstrate_limitations():
    """演示N-gram的局限性"""
    print("=" * 60)
    print("N-gram模型的局限性")
    print("=" * 60)
    print()

    corpus = "I love dogs I love cats I love birds"
    model = NGramModel(n=2)
    model.train(corpus)

    print("训练语料:", corpus)
    print()

    # 局限性1: 数据稀疏性
    print("【局限性1: 数据稀疏性】")
    print("问题: 如果测试集的n-gram在训练集中未出现,概率为0")

    test_cases = [
        "I love dogs",    # 在训练集中
        "I love rabbits", # "rabbits"未在训练集中
        "I hate dogs",    # "hate"未在训练集中
    ]

    for sent in test_cases:
        prob = model.sentence_probability(sent)
        status = "✓" if prob > 0 else "✗"
        print(f"  {status} P('{sent}') = {prob:.6f}")
    print()

    # 局限性2: 缺乏语义理解
    print("【局限性2: 缺乏语义理解】")
    print("问题: 模型无法理解语义相似的词(如dogs vs puppies)")

    similar_words = [
        "I love dogs",
        "I love puppies",  # 语义相似,但puppies未在训练集中
        "I love canines",  # canines是dogs的科学名称
    ]

    for sent in similar_words:
        prob = model.sentence_probability(sent)
        print(f"  P('{sent}') = {prob:.6f}")
    print()

    print("结论: N-gram模型无法泛化到未见过的词组合")
    print()

    # 局限性3: 长距离依赖
    print("【局限性3: 长距离依赖】")
    print("问题: Bigram只能看到前1个词,无法捕捉长距离依赖")

    long_sentence = "I love dogs but I hate cats"
    print(f"句子: '{long_sentence}'")
    print("问题: 模型在预测'hate'时,只看到了'cats',而不知道前面有'love'")
    print()


def main():
    """主函数"""
    # 演示Bigram
    demonstrate_bigram()

    # 演示Trigram
    demonstrate_trigram()

    # 演示局限性
    demonstrate_limitations()

    print("=" * 60)
    print("总结")
    print("=" * 60)
    print("""
N-gram语言模型:
  优点:
    - 简单直观,易于实现
    - 计算效率高
    - 在小数据集上表现尚可

  缺点:
    - 数据稀疏性:未见过的n-gram概率为0
    - 泛化能力差:无法理解语义相似性
    - 长距离依赖:无法捕捉长距离的依赖关系
    - 维数灾难:n越大,需要的数据量呈指数增长

  这就是为什么现代语言模型转向神经网络的原因!
    """)


if __name__ == '__main__':
    main()

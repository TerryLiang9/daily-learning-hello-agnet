"""
BPE (Byte Pair Encoding) 分词算法演示
======================================

展示子词分词算法的核心思想:
1. 从字符级别开始迭代合并
2. 基于频率的贪心合并策略
3. 平衡词表大小和语义表达

作者: DataWhale Hello-Agents学习项目
"""

import re
import collections
from typing import Dict, List, Tuple


class BPE:
    """字节对编码分词器"""

    def __init__(self, vocab_size: int = 10):
        """
        初始化BPE
        Args:
            vocab_size: 目标词表大小
        """
        self.vocab_size = vocab_size
        self.vocab = []  # 词表(包含合并后的子词)
        self.merge_rules = []  # 合并规则列表

    def train(self, corpus: Dict[str, int]):
        """
        训练BPE分词器
        Args:
            corpus: 语料库,格式为 {单词: 频次}
                   注意:单词末尾需要添加</w>标记
        """
        # 初始化:将单词拆分成字符序列
        vocab = {word: count for word, count in corpus.items()}

        print(f"初始词表({len(vocab)}个单词):")
        for word in list(vocab.keys())[:5]:
            print(f"  {word}")
        if len(vocab) > 5:
            print(f"  ... (共{len(vocab)}个单词)")
        print()

        # 初始词表是所有字符
        self.vocab = set()
        for word in vocab.keys():
            for char in word.split():
                self.vocab.add(char)

        print(f"初始字符集({len(self.vocab)}个): {' '.join(sorted(self.vocab))}")
        print()

        # 迭代合并
        num_merges = self.vocab_size - len(self.vocab)
        print(f"计划进行 {num_merges} 次合并")
        print("-" * 60)

        for i in range(num_merges):
            # 统计相邻符号对的频率
            pairs = self._get_stats(vocab)
            if not pairs:
                break

            # 选择频率最高的对
            best_pair = max(pairs, key=pairs.get)

            # 合并
            vocab = self._merge_vocab(best_pair, vocab)

            # 记录合并规则
            self.merge_rules.append(best_pair)
            merged_symbol = ''.join(best_pair)
            self.vocab.add(merged_symbol)

            # 显示进度
            print(f"第{i + 1}次合并: {best_pair[0]} + {best_pair[1]} → {merged_symbol}")
            print(f"  出现次数: {pairs[best_pair]}")
            print(f"  当前词表大小: {len(self.vocab)}")

            # 显示部分词汇变化
            sample_words = list(vocab.keys())[:3]
            print(f"  示例单词: {' '.join(sample_words)}")
            print()

    def _get_stats(self, vocab: Dict[str, int]) -> Dict[Tuple[str, str], int]:
        """统计所有相邻符号对的频率"""
        pairs = collections.defaultdict(int)
        for word, freq in vocab.items():
            symbols = word.split()
            for i in range(len(symbols) - 1):
                pairs[(symbols[i], symbols[i + 1])] += freq
        return pairs

    def _merge_vocab(self, pair: Tuple[str, str], vocab: Dict[str, int]) -> Dict[str, int]:
        """合并词汇表中的指定符号对"""
        new_vocab = {}
        bigram = re.escape(' '.join(pair))
        pattern = re.compile(r'(?<!\S)' + bigram + r'(?!\S)')

        for word in vocab:
            # 替换所有出现的位置
            new_word = pattern.sub(''.join(pair), word)
            new_vocab[new_word] = vocab[word]

        return new_vocab

    def tokenize(self, word: str) -> List[str]:
        """
        对新单词进行分词
        Args:
            word: 输入单词
        Returns:
            子词列表
        """
        # 添加结束标记
        word = word + '</w>'
        word = word.replace(' ', '</w> </w> ')  # 处理空格

        # 初始化:按字符拆分
        word_tokens = word.split()

        # 应用所有合并规则
        while True:
            merged = False
            for pair in self.merge_rules:
                # 查找可以合并的位置
                for i in range(len(word_tokens) - 1):
                    if word_tokens[i] == pair[0] and word_tokens[i + 1] == pair[1]:
                        # 合并
                        word_tokens[i:i + 2] = [''.join(pair)]
                        merged = True
                        break
                if merged:
                    break

            if not merged:
                break

        return word_tokens


def demonstrate_bpe_basic():
    """基础BPE演示"""
    print("=" * 60)
    print("BPE算法基础演示")
    print("=" * 60)
    print()

    # 创建迷你语料库
    corpus = {
        'h u g </w>': 1,
        'p u g </w>': 1,
        'p u n </w>': 1,
        'b u n </w>': 1
    }

    print("训练语料:")
    for word, freq in corpus.items():
        print(f"  '{word}': {freq}次")
    print()

    # 训练BPE
    bpe = BPE(vocab_size=10)
    bpe.train(corpus)

    print("=" * 60)
    print("分词结果")
    print("=" * 60)
    print()

    # 对新词进行分词
    test_words = ['bug', 'hug', 'pun', 'bun', 'pug']

    for word in test_words:
        tokens = bpe.tokenize(word)
        print(f"'{word}' → {' '.join(tokens)}")

    print()


def demonstrate_bpe_realistic():
    """更真实的BPE演示"""
    print("=" * 60)
    print("BPE算法真实场景演示")
    print("=" * 60)
    print()

    # 模拟一个更真实的语料库
    corpus = {
        'l o w </w>': 5,
        'l o w e s t </w>': 2,
        'n e w e r </w>': 6,
        'w i d e r </w>': 3,
        'n e w </w>': 2,
    }

    print("训练语料(常见英文单词):")
    # 显示原始单词
    original_words = ['low', 'lowest', 'newer', 'wider', 'new']
    for i, (word, freq) in enumerate(zip(original_words, [5, 2, 6, 3, 2])):
        print(f"  '{word}': {freq}次")
    print()

    # 训练BPE,目标词表大小15
    bpe = BPE(vocab_size=15)
    bpe.train(corpus)

    print("=" * 60)
    print("合并规则总结")
    print("=" * 60)
    print()
    for i, rule in enumerate(bpe.merge_rules, 1):
        print(f"  {i}. {rule[0]} + {rule[1]} = {''.join(rule)}")
    print()

    print("=" * 60)
    print("分词结果")
    print("=" * 60)
    print()

    # 测试分词
    test_words = ['low', 'lowest', 'newer', 'wider', 'new', 'lower']

    print("训练集中的词:")
    for word in test_words[:5]:
        tokens = bpe.tokenize(word)
        print(f"  '{word:8s}' → {' '.join(tokens)}")

    print("\n训练集外的词(OOV):")
    tokens = bpe.tokenize('lower')
    print(f"  'lower'    → {' '.join(tokens)}")
    print("  (说明: lower虽然不在训练集中,但可以通过子词组合lo + w + er来表示)")
    print()


def demonstrate_bpe_comparison():
    """对比BPE与其他分词方法"""
    print("=" * 60)
    print("BPE vs 字符级 vs 词级分词对比")
    print("=" * 60)
    print()

    # 训练一个简单的BPE
    corpus = {
        'u n h a p p y </w>': 1,
        'h a p p y </w>': 2,
        'u n s t a b l e </w>': 1,
        's t a b l e </w>': 1,
    }

    bpe = BPE(vocab_size=15)
    bpe.train(corpus)

    test_words = ['unhappy', 'happy', 'unstable']

    print("分词对比:")
    print(f"{'单词':12s} {'字符级':20s} {'词级':12s} {'BPE':20s}")
    print("-" * 64)

    for word in test_words:
        # 字符级
        char_level = ' '.join(list(word))

        # 词级(假设单词在词表中)
        word_level = word if word in ['happy', 'stable'] else '<UNK>'

        # BPE
        bpe_level = ' '.join(bpe.tokenize(word))

        print(f"{word:12s} {char_level:20s} {word_level:12s} {bpe_level:20s}")

    print()
    print("说明:")
    print("  - 字符级:词表小,但语义信息少,序列长度长")
    print("  - 词级:语义完整,但词表大,存在OOV问题")
    print("  - BPE:平衡词表大小和语义,能处理OOV词")
    print()


def main():
    """主函数"""
    # 基础演示
    demonstrate_bpe_basic()

    # 真实场景演示
    demonstrate_bpe_realistic()

    # 对比演示
    demonstrate_bpe_comparison()

    print("=" * 60)
    print("BPE算法总结")
    print("=" * 60)
    print("""
核心思想:
  1. 从字符级别开始,迭代合并高频的相邻符号对
  2. 贪心策略:每次选择频率最高的对进行合并
  3. 直到词表达到目标大小

优势:
  ✓ 词表大小可控
  ✓ 能处理未见过的词(OOV问题)
  ✓ 保留了单词内部的子结构信息
  ✓ 常见词保持完整,罕见词分解为子词

应用:
  - GPT系列模型
  - GPT-2, GPT-3, GPT-4
  - 许多现代LLM的基础

局限性:
  ✗ 纯基于频率,未考虑语义
  ✗ 对某些语言(如中文)效果有限
  ✗ 需要预处理(如SentencePiece的改进)

现代发展:
  → WordPiece(BERT使用,基于语言模型概率)
  → SentencePiece(统一处理空格,语言无关)
  → Unigram(基于子词删除而非添加)
    """)


if __name__ == '__main__':
    main()

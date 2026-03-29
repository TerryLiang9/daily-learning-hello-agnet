"""
词嵌入演示
============

展示词向量如何捕捉语义关系:
1. 简化的2D词向量空间
2. 余弦相似度计算
3. 类比推理(King - Man + Woman = Queen)

作者: DataWhale Hello-Agents学习项目
"""

import numpy as np
from typing import Dict, List, Tuple
import json
import sys
import io

# 修复 Windows 终端编码问题
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


class WordEmbeddingDemo:
    """词嵌入演示"""

    def __init__(self):
        """初始化词嵌入"""
        # 构造一个简化的2D词向量空间
        # 在实际应用中,词向量是通过Word2Vec、GloVe等算法在高维空间(300D+)学习得到的
        self.embeddings = self._create_demo_embeddings()

    def _create_demo_embeddings(self) -> Dict[str, np.ndarray]:
        """
        创建演示用的词向量
        这些向量是手工构造的,用于演示概念
        在实际应用中,这些向量是通过神经网络训练得到的
        """
        embeddings = {
            # 皇室相关词(第一维高表示皇室属性)
            "king": np.array([0.9, 0.8]),
            "queen": np.array([0.9, 0.2]),
            "prince": np.array([0.7, 0.8]),
            "princess": np.array([0.7, 0.2]),

            # 性别相关词(第二维表示性别:1=男性,0=女性)
            "man": np.array([0.2, 0.9]),
            "woman": np.array([0.2, 0.3]),
            "boy": np.array([0.1, 0.85]),
            "girl": np.array([0.1, 0.35]),

            # 职业相关
            "doctor": np.array([0.5, 0.6]),
            "nurse": np.array([0.5, 0.4]),
            "engineer": np.array([0.4, 0.7]),
            "teacher": np.array([0.4, 0.5]),
        }
        return embeddings

    def cosine_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """
        计算余弦相似度
        Args:
            vec1, vec2: 词向量
        Returns:
            相似度(范围[-1, 1],1表示完全相同,0表示正交,-1表示完全相反)
        """
        dot_product = np.dot(vec1, vec2)
        norm_product = np.linalg.norm(vec1) * np.linalg.norm(vec2)

        if norm_product == 0:
            return 0.0

        return dot_product / norm_product

    def find_similar_words(self, word: str, top_k: int = 3) -> List[Tuple[str, float]]:
        """
        找到最相似的词
        Args:
            word: 目标词
            top_k: 返回前k个最相似的词
        Returns:
            [(相似词, 相似度), ...]
        """
        if word not in self.embeddings:
            return []

        target_vec = self.embeddings[word]
        similarities = []

        for other_word, other_vec in self.embeddings.items():
            if other_word == word:
                continue

            sim = self.cosine_similarity(target_vec, other_vec)
            similarities.append((other_word, sim))

        # 按相似度降序排序
        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities[:top_k]

    def word_analogy(self, word1: str, word2: str, word3: str) -> Tuple[str, float]:
        """
        词类比推理
        计算: word1 - word2 + word3 = ?
        例如: king - man + woman = queen

        Args:
            word1, word2, word3: 输入词
        Returns:
            (结果词, 相似度)
        """
        if word1 not in self.embeddings or word2 not in self.embeddings or word3 not in self.embeddings:
            return None, 0.0

        # 计算目标向量
        target_vec = self.embeddings[word1] - self.embeddings[word2] + self.embeddings[word3]

        # 找到最接近的词
        best_word = None
        best_similarity = -1

        for word, vec in self.embeddings.items():
            if word in [word1, word2, word3]:
                continue

            sim = self.cosine_similarity(target_vec, vec)
            if sim > best_similarity:
                best_similarity = sim
                best_word = word

        return best_word, best_similarity

    def visualize_2d_space(self):
        """可视化2D词向量空间(ASCII艺术)"""
        print("\n2D词向量空间可视化:")
        print("=" * 50)
        print("Y轴: 性别 (1.0=男性, 0.0=女性)")
        print("X轴: 皇室 (1.0=皇室, 0.0=平民)")
        print("=" * 50)

        # 创建网格
        grid_size = 10
        grid = [[' ' for _ in range(grid_size)] for _ in range(grid_size)]

        # 标记单词位置
        word_positions = {}
        for word, vec in self.embeddings.items():
            x = int(vec[0] * (grid_size - 1))
            y = int(vec[1] * (grid_size - 1))
            word_positions[word] = (x, y)

        # 打印网格
        for y in range(grid_size - 1, -1, -1):
            row = f"{y * 0.1:.1f} |"
            for x in range(grid_size):
                # 找到这个位置上的词
                word_here = None
                for word, (wx, wy) in word_positions.items():
                    if wx == x and wy == y:
                        word_here = word
                        break

                if word_here:
                    row += word_here[0].upper()  # 只显示首字母
                else:
                    row += '·'
                row += ' '
            print(row)

        # X轴标签
        print("    " + "-" * (grid_size * 2))
        x_labels = "   "
        for x in range(grid_size):
            x_labels += f"{x * 0.1:.0f} "
        print(x_labels)
        print()

        # 图例
        print("图例:")
        for word, (x, y) in word_positions.items():
            print(f"  {word[0].upper()}: {word:10s} at ({x*0.1:.1f}, {y*0.1:.1f})")
        print()


def demonstrate_similarity():
    """演示词相似度"""
    print("=" * 60)
    print("演示1: 词相似度计算")
    print("=" * 60)
    print()

    demo = WordEmbeddingDemo()

    test_words = [
        ("king", "queen"),
        ("king", "man"),
        ("king", "doctor"),
        ("man", "woman"),
        ("doctor", "nurse"),
    ]

    print("词对相似度:")
    for word1, word2 in test_words:
        vec1 = demo.embeddings[word1]
        vec2 = demo.embeddings[word2]
        sim = demo.cosine_similarity(vec1, vec2)

        # 可视化相似度
        bar = "█" * int(sim * 40)
        print(f"  sim('{word1}', '{word2}') = {sim:.3f} {bar}")

    print()


def demonstrate_nearest_neighbors():
    """演示最近邻查找"""
    print("=" * 60)
    print("演示2: 最近邻查找")
    print("=" * 60)
    print()

    demo = WordEmbeddingDemo()

    target_words = ["king", "doctor", "man"]

    for word in target_words:
        similar = demo.find_similar_words(word, top_k=3)
        print(f"'{word}' 的最相似的词:")
        for similar_word, sim in similar:
            bar = "█" * int(sim * 30)
            print(f"  {similar_word:10s}: {sim:.3f} {bar}")
        print()


def demonstrate_analogy():
    """演示词类比推理"""
    print("=" * 60)
    print("演示3: 词类比推理")
    print("=" * 60)
    print()

    demo = WordEmbeddingDemo()

    # 经典类比: king - man + woman = queen
    print("【经典案例:性别类比】")
    print("类比: king - man + woman = ?")

    result, sim = demo.word_analogy("king", "man", "woman")
    print(f"计算: vector('king') - vector('man') + vector('woman')")
    print(f"结果: '{result}' (相似度: {sim:.3f})")

    # 验证
    if result == "queen":
        print("✓ 正确! queen正是queen(女王)")

        # 显示向量计算过程
        king_vec = demo.embeddings["king"]
        man_vec = demo.embeddings["man"]
        woman_vec = demo.embeddings["woman"]
        queen_vec = demo.embeddings["queen"]
        result_vec = king_vec - man_vec + woman_vec

        print(f"\n向量:")
        print(f"  king   = {king_vec}")
        print(f"  man    = {man_vec}")
        print(f"  woman  = {woman_vec}")
        print(f"  - man + woman = {result_vec}")
        print(f"  queen  = {queen_vec}")
        print(f"  相似度 = {demo.cosine_similarity(result_vec, queen_vec):.3f}")

    print()

    # 更多类比案例
    analogies = [
        ("prince", "man", "woman", "princess"),
        ("king", "queen", "prince", "prince"),
    ]

    print("【更多类比案例】")
    for word1, word2, word3, expected in analogies:
        result, sim = demo.word_analogy(word1, word2, word3)
        status = "✓" if result == expected else "✗"
        print(f"{status} {word1} - {word2} + {word3} = {result} (期望: {expected}, 相似度: {sim:.3f})")

    print()


def main():
    """主函数"""
    print("\n")
    print("█" * 60)
    print("█" + " " * 18 + "词嵌入演示" + " " * 18 + "█")
    print("█" * 60)
    print("\n")

    # 初始化演示
    demo = WordEmbeddingDemo()

    # 可视化词向量空间
    demo.visualize_2d_space()

    # 演示1: 相似度
    demonstrate_similarity()

    # 演示2: 最近邻
    demonstrate_nearest_neighbors()

    # 演示3: 类比推理
    demonstrate_analogy()

    print("=" * 60)
    print("总结")
    print("=" * 60)
    print("""
词嵌入的核心思想:
  ✓ 将词映射到连续向量空间
  ✓ 语义相似的词在空间中距离近
  ✓ 可以通过向量运算捕捉语义关系

关键优势:
  ✓ 解决N-gram的语义盲点
  ✓ 可以泛化到未见过的词
  ✓ 捕捉复杂的语义关系

实际应用:
  - Word2Vec (CBOW, Skip-gram)
  - GloVe (全局词向量)
  - FastText (子词信息)
  - 现代LLM的嵌入层

注意:
  演示中的向量是手工构造的简化版本。
  实际应用中,词向量是通过神经网络在
  大规模语料上训练得到的,维度通常在300+
    """)


if __name__ == '__main__':
    main()

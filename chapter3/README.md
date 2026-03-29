# 第三章 大语言模型基础 - 实践项目

本章节包含多个实践项目,帮助深入理解大语言模型的工作原理:

## 项目一:语言模型演进演示

从N-gram到神经网络的完整实现演示。

### 包含内容

1. **N-gram语言模型**
   - Bigram/Trigram概率计算
   - 最大似然估计
   - 马尔可夫假设演示

2. **词嵌入可视化**
   - Word2Vec风格词向量
   - 余弦相似度计算
   - 类比推理演示(King - Man + Woman = Queen)

3. **BPE分词算法**
   - 字节对编码实现
   - 词表构建过程
   - 子词切分演示

### 运行方法

```bash
# N-gram演示
python ngram_demo.py

# 词嵌入演示
python word_embedding_demo.py

# BPE分词演示
python bpe_demo.py
```

---

## 项目二:本地LLM部署与提示工程

使用开源模型进行提示工程实验。

### 环境配置

```bash
pip install -r requirements.txt
```

### 功能演示

1. **模型加载与推理**
   - 使用Hugging Face Transformers
   - 支持CPU/GPU自动切换
   - 多种开源模型兼容(Qwen, Llama, ChatGLM等)

2. **提示工程实验**
   - Zero-shot vs Few-shot对比
   - 思维链(CoT)提示
   - 角色扮演提示
   - 采样参数调优(temperature, top_p, top_k)

3. **分词器实验**
   - Token计数与成本估算
   - 中英文分词差异
   - 特殊Token处理

### 运行方法

```bash
# 基础对话示例
python llm_chat.py

# 提示工程实验
python prompt_engineering_lab.py

# 分词器分析工具
python tokenizer_analyzer.py
```

---

## 项目三:Transformer架构演示

Transformer核心组件的简化实现。

### 包含模块

1. **自注意力机制**
   - Scaled Dot-Product Attention
   - 多头注意力
   - 可视化注意力权重

2. **位置编码**
   - 正弦/余弦位置编码
   - 可学习位置编码

3. **完整Transformer层**
   - Encoder层实现
   - Decoder层实现
   - 前馈网络

### 运行方法

```bash
python transformer_demo.py
```

---

## 📖 学习重点

### 1. 语言模型的核心任务
- **定义**: 计算词序列出现的概率
- **应用**: 语音识别、机器翻译、文本生成
- **演进**: N-gram → 神经网络LM → RNN/LSTM → Transformer

### 2. Transformer的革命性创新
- **自注意力机制**: 并行计算,捕捉长距离依赖
- **位置编码**: 补充序列顺序信息
- **Encoder-Decoder架构**: 理解与生成分离
- **Decoder-Only**: GPT系列的简化设计

### 3. 提示工程关键技巧
- **Zero-shot**: 直接指令
- **Few-shot**: 提供示例
- **CoT**: 逐步推理
- **角色扮演**: 设定专家身份

### 4. 模型选型考虑
- **性能**: 准确性、推理能力
- **成本**: API费用、硬件需求
- **速度**: 延迟、吞吐量
- **上下文窗口**: 最大Token数
- **部署方式**: API vs 本地
- **生态支持**: 工具链、社区

---

## 🎯 实践习题

### 习题1: N-gram实践

使用提供的迷你语料库(`datawhale agent learns`, `datawhale agent works`):
1. 计算句子 `agent works` 在Bigram模型下的概率
2. 对比Bigram和Trigram的差异
3. 解释N-gram模型的根本局限性

### 习题2: 提示策略对比

选择一个具体任务(如情感分类、代码生成):
1. 设计Zero-shot提示
2. 设计Few-shot提示(3个示例)
3. 设计思维链提示
4. 对比三种策略的效果差异

### 习题3: 模型选型分析

假设你要构建以下智能体,如何选择模型?
1. **客服智能体**: 成本敏感,需7×24运行
2. **代码审查助手**: 需要强大的代码理解能力
3. **企业知识问答**: 数据敏感,需本地部署

### 习题4: 幻觉问题缓解

研究并实现至少一种缓解模型幻觉的方法:
1. RAG(检索增强生成)
2. 多步推理与验证
3. 外部工具调用

---

## 📚 相关资源

- [Transformer论文](https://arxiv.org/abs/1706.03762)
- [Attention is All You Need](https://papers.nips.cc/paper/2017/hash/3f5ee243547dee91fbd053c1c4a845aa-Abstract.html)
- [Hugging Face Models](https://huggingface.co/models)
- [DataWhale Hello-Agents教程](https://github.com/datawhalechina/hello-agents)

---

## 💡 代码结构

```
chapter3/
├── README.md                    # 本文档
├── requirements.txt             # 依赖包
│
├── ngram_demo.py               # N-gram语言模型演示
├── word_embedding_demo.py      # 词嵌入演示
├── bpe_demo.py                 # BPE分词算法演示
│
├── llm_chat.py                 # 基础对话示例
├── prompt_engineering_lab.py   # 提示工程实验室
├── tokenizer_analyzer.py       # 分词器分析工具
│
└── transformer_demo.py         # Transformer架构演示
```

---

**祝你学习愉快!** 🎉

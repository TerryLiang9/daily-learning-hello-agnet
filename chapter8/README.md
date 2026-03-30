# 第八章：记忆与检索

> 构建智能体的记忆系统和RAG应用

**本章重点**：
- 理解记忆的类型和作用
- 实现向量检索系统
- 构建RAG（检索增强生成）应用

---

## 学习笔记

### 8.1 记忆的类型

```
记忆系统
├── 感知记忆 (Sensory Memory)
├── 工作记忆 (Working Memory)
├── 短期记忆 (Short-term Memory)
└── 长期记忆 (Long-term Memory)
```

| 记忆类型 | 容量 | 持续时间 | 作用 |
|---------|------|---------|------|
| 感知记忆 | 极小 | < 1秒 | 暂存感官信息 |
| 工作记忆 | 7±2项 | < 30秒 | 当前任务处理 |
| 短期记忆 | 有限 | 数分钟到数天 | 近期经验 |
| 长期记忆 | 无限 | 永久 | 知识和技能 |

### 8.2 RAG架构

```
用户问题
   ↓
向量检索 → 相关文档
   ↓
文档 + 问题 → LLM → 回答
```

**核心优势**：
- 减少幻觉
- 提供可追溯的答案来源
- 可以更新知识而不重新训练模型

---

## 实现代码

### 1. 向量存储

```python
# vector_store.py

from typing import List, Dict, Optional
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


class VectorStore:
    """简单的向量存储"""

    def __init__(self, embedding_dim: int = 768):
        self.embedding_dim = embedding_dim
        self.vectors = []
        self.documents = []

    def add(self, document: str, vector: np.ndarray):
        """添加文档和向量"""
        if vector.shape[-1] != self.embedding_dim:
            raise ValueError(f"向量维度不匹配，期望 {self.embedding_dim}")

        self.vectors.append(vector)
        self.documents.append(document)

    def search(self, query_vector: np.ndarray, top_k: int = 5) -> List[Dict]:
        """搜索最相似的文档"""
        if not self.vectors:
            return []

        # 计算相似度
        similarities = cosine_similarity(
            [query_vector],
            self.vectors
        )[0]

        # 排序并返回top_k
        top_indices = np.argsort(similarities)[::-1][:top_k]

        results = []
        for idx in top_indices:
            results.append({
                "document": self.documents[idx],
                "score": float(similarities[idx])
            })

        return results

    def save(self, filepath: str):
        """保存向量存储"""
        import pickle

        with open(filepath, "wb") as f:
            pickle.dump({
                "vectors": self.vectors,
                "documents": self.documents,
                "embedding_dim": self.embedding_dim
            }, f)

    def load(self, filepath: str):
        """加载向量存储"""
        import pickle

        with open(filepath, "rb") as f:
            data = pickle.load(f)
            self.vectors = data["vectors"]
            self.documents = data["documents"]
            self.embedding_dim = data["embedding_dim"]
```

### 2. RAG系统

```python
# rag_system.py

from typing import List, Dict, Optional
from vector_store import VectorStore


class RAGSystem:
    """检索增强生成系统"""

    def __init__(self, llm_client, embedding_model, vector_store: Optional[VectorStore] = None):
        self.llm_client = llm_client
        self.embedding_model = embedding_model
        self.vector_store = vector_store or VectorStore()

    def add_document(self, document: str):
        """添加文档到知识库"""
        # 生成embedding
        embedding = self._get_embedding(document)

        # 存储到向量库
        self.vector_store.add(document, embedding)

    def _get_embedding(self, text: str) -> np.ndarray:
        """获取文本的向量表示"""
        # 这里使用简单的模型，实际可使用OpenAI embeddings或其他
        # 示例：使用sentence-transformers
        from sentence_transformers import SentenceTransformer

        if isinstance(self.embedding_model, str):
            model = SentenceTransformer(self.embedding_model)
            self.embedding_model = model

        return self.embedding_model.encode(text)

    def query(self, question: str, top_k: int = 3) -> str:
        """查询问题并生成答案"""
        # 1. 检索相关文档
        question_embedding = self._get_embedding(question)
        relevant_docs = self.vector_store.search(question_embedding, top_k)

        # 2. 构建上下文
        context = self._build_context(relevant_docs)

        # 3. 生成答案
        answer = self._generate_answer(question, context)

        return answer

    def _build_context(self, relevant_docs: List[Dict]) -> str:
        """构建上下文"""
        context_parts = []
        for i, doc in enumerate(relevant_docs, 1):
            context_parts.append(
                f"[文档 {i}] (相似度: {doc['score']:.2f})\n{doc['document']}\n"
            )
        return "\n".join(context_parts)

    def _generate_answer(self, question: str, context: str) -> str:
        """生成答案"""
        prompt = f"""
基于以下文档内容回答问题。如果文档中没有相关信息，请说明。

{context}

问题：{question}

答案：
"""

        messages = [{"role": "user", "content": prompt}]
        response = self.llm_client.think(messages)

        return response

    def load_documents(self, filepath: str):
        """从文件加载文档"""
        import os

        if os.path.isfile(filepath):
            # 单个文件
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
                self.add_document(content)
        else:
            # 目录
            for filename in os.listdir(filepath):
                if filename.endswith(".txt"):
                    file_path = os.path.join(filepath, filename)
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                        self.add_document(content)
```

### 3. 使用示例

```python
# example_rag.py

from rag_system import RAGSystem
from llm_client import HelloAgentsLLM

# 初始化
llm = HelloAgentsLLM()
rag = RAGSystem(
    llm_client=llm,
    embedding_model="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)

# 添加文档
documents = [
    "Python是一种高级编程语言，由Guido van Rossum于1991年创建。",
    "机器学习是人工智能的一个分支，它使计算机能够从数据中学习。",
    "深度学习是机器学习的一个子集，使用神经网络模拟人脑。"
]

for doc in documents:
    rag.add_document(doc)

# 查询
question = "什么是深度学习？"
answer = rag.query(question)

print(f"问题：{question}")
print(f"答案：{answer}")
```

---

## 实践项目

### 项目：智能文档问答系统

**目标**：构建一个能够回答PDF文档问题的系统

```python
# pdf_qa_system.py

import os
from typing import List
from rag_system import RAGSystem
from llm_client import HelloAgentsLLM


class DocumentQASystem:
    """文档问答系统"""

    def __init__(self, llm_client, embedding_model):
        self.rag = RAGSystem(llm_client, embedding_model)

    def load_pdf(self, pdf_path: str):
        """加载PDF文件"""
        # 这里使用PyPDF2提取文本
        import PyPDF2

        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text()

        # 分块处理
        chunks = self._split_text(text, chunk_size=500)
        for chunk in chunks:
            self.rag.add_document(chunk)

    def _split_text(self, text: str, chunk_size: int = 500) -> List[str]:
        """将文本分割成块"""
        chunks = []
        words = text.split()
        current_chunk = []

        for word in words:
            current_chunk.append(word)
            if len(" ".join(current_chunk)) >= chunk_size:
                chunks.append(" ".join(current_chunk))
                current_chunk = []

        if current_chunk:
            chunks.append(" ".join(current_chunk))

        return chunks

    def ask(self, question: str) -> Dict:
        """提问"""
        answer = self.rag.query(question)

        return {
            "question": question,
            "answer": answer
        }


# 使用示例
if __name__ == "__main__":
    # 初始化
    llm = HelloAgentsLLM()
    qa_system = DocumentQASystem(
        llm_client=llm,
        embedding_model="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    )

    # 加载文档
    qa_system.load_pdf("example.pdf")

    # 提问
    questions = [
        "这个文档主要讲什么？",
        "文档中提到了哪些关键概念？"
    ]

    for q in questions:
        result = qa_system.ask(q)
        print(f"问题: {result['question']}")
        print(f"答案: {result['answer']}\n")
```

---

## 学习总结

### 核心概念

1. **向量表示**：将文本转换为数值向量
2. **相似度计算**：衡量文本相关程度
3. **检索增强**：结合检索和生成

### 技术栈

- **向量数据库**：Chroma, FAISS, Pinecone
- **Embedding模型**：OpenAI embeddings, Sentence-BERT
- **LLM**：GPT-4, Claude, Llama

### 最佳实践

1. 文档分块策略
2. Metadata管理
3. 混合检索（关键词+向量）
4. 重排序优化

---

## 参考资源

- [LangChain RAG教程](https://python.langchain.com/docs/use_cases/question_answering)
- [Chroma文档](https://docs.trychroma.com/)
- [Sentence-Transformers](https://www.sbert.net/)

---

## 许可证

MIT License

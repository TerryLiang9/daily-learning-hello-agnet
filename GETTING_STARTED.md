# 🚀 快速开始指南

欢迎来到DataWhale Hello-Agents学习项目！本指南将帮助你快速开始。

## 📋 目录

1. [环境准备](#环境准备)
2. [章节导航](#章节导航)
3. [推荐学习路径](#推荐学习路径)
4. [常见问题](#常见问题)
5. [进阶资源](#进阶资源)

---

## 环境准备

### 1. Python环境

确保你的Python版本 >= 3.8：

```bash
python --version
```

### 2. 安装依赖

根据你要学习的章节安装相应依赖：

```bash
# 第四章依赖（ReAct等）
pip install -r chapter4/requirements.txt

# 第八章依赖（RAG系统）
pip install sentence-transformers scikit-learn

# 其他章节
pip install openai python-dotenv langchain langgraph
```

### 3. 配置API密钥

创建 `.env` 文件并配置你的API密钥：

```bash
# .env 文件示例
LLM_API_KEY=your-api-key-here
LLM_MODEL_ID=your-model-name
LLM_BASE_URL=https://api.example.com/v1

# 第四章需要额外配置
SERPAPI_API_KEY=your-serpapi-key-here
```

---

## 章节导航

### 🌟 推荐从这些章节开始

#### 第一章：初识智能体
```bash
cd chapter1
python agent.py
```
**适合人群**：所有初学者
**学习时长**：2-3小时

#### 第四章：智能体经典范式
```bash
cd chapter4
python react_agent.py
```
**适合人群**：有一定编程基础的学习者
**学习时长**：4-6小时

#### 第八章：记忆与检索（RAG）
```bash
# 阅读chapter8/README.md了解原理
```
**适合人群**：想深入理解AI应用的学习者
**学习时长**：3-4小时

### 📚 所有章节概览

| 章节 | 难度 | 代码量 | 学习时长 |
|------|------|--------|----------|
| 第一章 | ⭐ | 中等 | 2-3小时 |
| 第二章 | ⭐ | 少 | 1-2小时 |
| 第三章 | ⭐⭐ | 中等 | 2-3小时 |
| 第四章 | ⭐⭐⭐ | 多 | 4-6小时 |
| 第五章 | ⭐ | 少 | 1-2小时 |
| 第六章 | ⭐⭐⭐ | 多 | 3-4小时 |
| 第七章 | ⭐⭐⭐⭐ | 多 | 4-5小时 |
| 第八章 | ⭐⭐⭐⭐ | 多 | 3-4小时 |
| 第九章-第十二章 | ⭐⭐⭐⭐ | 中等 | 8-10小时 |
| 第十三章-第十六章 | ⭐⭐⭐⭐⭐ | 多 | 10-15小时 |

---

## 推荐学习路径

### 路径1：快速实践者（适合有经验的开发者）

```
第一章（1天）→ 第四章（2天）→ 第八章（1天）→ 第十三章（2天）→ 第十六章（2天）
```

**总时长**：约8天

### 路径2：系统学习者（适合初学者）

```
第一章 → 第二章 → 第三章 → 第四章 → 第五章 → 第六章
→ 第七章 → 第八章 → 第九章 → 第十章 → 第十一章
→ 第十二章 → 第十三章 → 第十四章 → 第十五章 → 第十六章
```

**总时长**：约2-3周

### 路径3：专题深入者（适合特定需求）

#### 想深入理解智能体原理：
```
第四章 → 第七章 → 第十章 → 第十二章 → 第十五章
```

#### 想快速开发应用：
```
第五章 → 第八章 → 第十三章 → 第十六章
```

#### 想做研究工作：
``
第六章 → 第十一章 → 第十四章 → 第十六章
```

---

## 常见问题

### Q1: 运行代码时提示API密钥错误？

**A**: 请确保：
1. 已创建 `.env` 文件
2. API密钥正确配置
3. `.env` 文件在正确的目录下

### Q2: 如何选择合适的LLM API？

**A**: 推荐选项：
- **国内用户**：智谱AI、通义千问、百度文心
- **国外用户**：OpenAI GPT-4、Claude
- **本地运行**：Ollama + Llama 3

### Q3: 第四章的SerpApi密钥如何获取？

**A**:
1. 访问 https://serpapi.com/
2. 注册免费账户
3. 在控制台获取API密钥
4. 添加到 `.env` 文件

### Q4: 代码运行报错怎么办？

**A**:
1. 检查Python版本（需要 >= 3.8）
2. 确保所有依赖已安装：`pip install -r requirements.txt`
3. 查看错误信息，检查配置文件
4. 在GitHub提Issue：https://github.com/TerryLiang9/daily-learning-hello-agnet/issues

### Q5: 如何修改代码以适配自己的需求？

**A**:
1. 理解原始代码的工作原理
2. 修改提示词（prompt）部分
3. 添加自己的工具或智能体
4. 参考第十六章的毕业设计框架

---

## 进阶资源

### 📚 推荐书籍

1. **《动手学深度学习》** - 李沐
2. **《自然语言处理综论》** - Daniel Jurafsky
3. **《重构：改善既有代码的设计》** - Martin Fowler

### 🎥 推荐课程

1. **DataWhale AI课程** - https://github.com/datawhalechina
2. **LangChain实战课** - DeepLearning.AI
3. **Prompt Engineering指南** - https://www.promptingguide.ai/

### 🔗 推荐网站

1. **Papers with Code** - https://paperswithcode.com/
2. **Hugging Face** - https://huggingface.co/
3. **ArXiv** - https://arxiv.org/list/cs.AI/recent

### 🛠️ 实用工具

1. **向量数据库**：Chroma, FAISS, Pinecone
2. **LLM监控**：LangSmith, Weights & Biases
3. **开发环境**：Jupyter Lab, VS Code
4. **API测试**：Postman, Insomnia

---

## 学习技巧

### 1. 动手实践
- 不要只看代码，一定要运行
- 修改参数，观察结果变化
- 尝试添加新功能

### 2. 记笔记
- 在代码中添加注释
- 记录遇到的问题和解决方案
- 总结每个章节的核心要点

### 3. 社区交流
- 加入DataWhale社区
- 参与GitHub讨论
- 写博客分享心得

### 4. 项目驱动
- 选择一个实际问题
- 运用所学知识解决
- 不断完善和优化

---

## 项目展示

### 展示你的学习成果

1. **GitHub仓库**
   - 完善README文档
   - 添加代码注释
   - 提交commit记录

2. **技术博客**
   - 总结学习心得
   - 分享项目经验
   - 讲解核心概念

3. **视频演示**
   - 录制项目运行视频
   - 制作讲解视频
   - 发布到B站/YouTube

---

## 下一步

完成所有章节学习后，你可以：

1. ✅ **完成毕业设计**（第十六章）
2. ✅ **参与开源项目**
3. ✅ **参加AI竞赛**
4. ✅ **发表论文**
5. ✅ **创业或求职**

---

## 联系方式

- **GitHub Issues**: https://github.com/TerryLiang9/daily-learning-hello-agnet/issues
- **Email**: your-email@example.com
- **微信**: your-wechat-id

---

## 更新日志

- **2026-03-30**: 完成全部16章内容
- **2026-03-29**: 完成第1-3章
- **2026-03-28**: 项目初始化

---

**祝你学习顺利！** 🎉

有问题随时提Issue，我们一起讨论进步！

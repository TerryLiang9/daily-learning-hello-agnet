# 🤝 贡献指南

感谢你对DataWhale Hello-Agents学习项目的关注！我们欢迎各种形式的贡献。

## 📋 目录

- [如何贡献](#如何贡献)
- [贡献类型](#贡献类型)
- [开发指南](#开发指南)
- [代码规范](#代码规范)
- [提交规范](#提交规范)
- [问题反馈](#问题反馈)

---

## 如何贡献

### 1. Fork仓库

点击GitHub页面右上角的"Fork"按钮

### 2. Clone到本地

```bash
git clone https://github.com/YOUR_USERNAME/daily-learning-hello-agnet.git
cd daily-learning-hello-agnet
```

### 3. 创建分支

```bash
git checkout -b feature/your-feature-name
```

### 4. 进行修改

按照下面的代码规范进行开发

### 5. 提交更改

```bash
git add .
git commit -m "feat: 添加你的功能描述"
```

### 6. 推送到你的Fork

```bash
git push origin feature/your-feature-name
```

### 7. 创建Pull Request

在GitHub上创建Pull Request

---

## 贡献类型

我们欢迎以下类型的贡献：

### 🐛 Bug修复

发现并修复代码中的问题

### ✨ 新功能

添加新的智能体实现或工具

### 📚 文档改进

- 修正错别字
- 补充说明
- 添加示例
- 翻译文档

### 🎨 代码优化

- 提高性能
- 改进可读性
- 减少重复代码

### 🧪 测试用例

添加单元测试或集成测试

### 💡 示例代码

提供更多的使用示例

---

## 开发指南

### 环境设置

```bash
# 克隆仓库
git clone https://github.com/YOUR_USERNAME/daily-learning-hello-agnet.git
cd daily-learning-hello-agnet

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r chapter4/requirements.txt
pip install -r chapter8/requirements.txt  # 如果需要
```

### 项目结构

```
daily-learning-hello-agnet/
├── chapter1/          # 基础章节
├── chapter4/          # 核心实现
├── chapter8/          # 高级功能
├── chapter13/         # 综合案例
└── ...
```

### 开发流程

1. **选择任务**
   - 查看Issues
   - 选择自己感兴趣的任务
   - 评论表明你要处理

2. **编写代码**
   - 遵循代码规范
   - 添加必要注释
   - 编写测试用例

3. **测试代码**
   ```bash
   # 运行测试
   python chapter4/react_agent.py
   python chapter4/plan_solve_agent.py
   # ... 其他测试
   ```

4. **更新文档**
   - 更新README
   - 添加使用示例
   - 记录API变更

---

## 代码规范

### Python代码风格

遵循PEP 8规范：

```python
# ✅ 好的示例
class ReActAgent:
    """ReAct智能体实现"""

    def __init__(self, llm_client, tool_executor):
        self.llm_client = llm_client
        self.tool_executor = tool_executor
        self.history = []

    def run(self, question: str) -> str:
        """运行智能体

        Args:
            question: 用户问题

        Returns:
            智能体的回答
        """
        # 实现代码
        pass


# ❌ 不好的示例
class reactagent:  # 类名应该用驼峰命名
    def __init__(self,lc,te):  # 参数名应该有描述性
        self.l=lc  # 属性名应该清晰
```

### 文档字符串规范

使用Google风格的文档字符串：

```python
def search(query: str, top_k: int = 5) -> List[Dict]:
    """搜索信息

    Args:
        query: 搜索查询字符串
        top_k: 返回结果数量，默认为5

    Returns:
        包含搜索结果的列表，每个结果是一个字典

    Raises:
        ValueError: 当query为空时

    Examples:
        >>> search("Python教程")
        [{'title': 'Python官方文档', 'url': '...'}]
    """
    pass
```

### 注释规范

```python
# ✅ 好的注释
# 检查智能体是否达到最大步数
if current_step >= self.max_steps:
    logger.warning("已达到最大步数限制")
    break

# ❌ 不好的注释
# i加1
i = i + 1
```

---

## 提交规范

### Commit Message格式

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Type类型

- `feat`: 新功能
- `fix`: Bug修复
- `docs`: 文档更新
- `style`: 代码格式（不影响功能）
- `refactor`: 重构
- `perf`: 性能优化
- `test`: 测试相关
- `chore`: 构建/工具链

### 示例

```
feat(chapter4): 添加ReAct智能体流式响应支持

- 实现流式输出功能
- 添加响应时间统计
- 更新使用文档

Closes #1
```

---

## 问题反馈

### 报告Bug

创建Issue时，请包含：

1. **问题描述**
   - 清晰简洁的标题
   - 详细的问题描述

2. **复现步骤**
   ```bash
   1. cd chapter4
   2. python react_agent.py
   3. 输入：华为最新手机
   4. 观察到：程序崩溃
   ```

3. **预期行为**
   - 应该发生什么

4. **环境信息**
   - Python版本：3.9
   - 操作系统：Windows 11
   - 依赖版本：openai 1.0.0

5. **日志/截图**
   - 错误信息
   - 相关截图

### 功能建议

提出新功能时，请说明：

1. **功能描述**
   - 这个功能做什么
   - 为什么需要它

2. **使用场景**
   - 在什么情况下使用
   - 解决什么问题

3. **实现建议**（可选）
   - 你认为如何实现
   - 有没有参考实现

---

## Pull Request指南

### PR标题

使用与Commit Message相同的格式

### PR描述模板

```markdown
## 变更说明
<!-- 简要描述这个PR做了什么 -->

## 变更类型
- [ ] Bug修复
- [ ] 新功能
- [ ] 代码重构
- [ ] 文档更新
- [ ] 性能优化

## 测试
<!-- 描述如何测试这些变更 -->

- [ ] 单元测试通过
- [ ] 手动测试通过
- [ ] 添加了新的测试用例

## 检查清单
- [ ] 代码遵循项目规范
- [ ] 添加了必要的注释
- [ ] 更新了相关文档
- [ ] 没有引入新的警告

## 相关Issue
Closes #issue_number
```

### 代码审查

我们会审查所有PR，可能要求：

1. 修改代码风格
2. 添加更多测试
3. 完善文档
4. 解释设计决策

请积极响应审查意见。

---

## 社区规范

### 行为准则

1. **尊重他人**
   - 友善交流
   - 建设性反馈
   - 包容不同观点

2. **专业态度**
   - 专注技术讨论
   - 基于事实交流
   - 避免人身攻击

3. **协作精神**
   - 乐于助人
   - 分享知识
   - 共同进步

### 获得认可

优秀的贡献者将获得：

1. ✨ 在Contributors列表中被列出
2. 🏆 项目维护者权限
3. 📝 项目文档中致谢
4. 💼 推荐信或工作机会

---

## 许可证

通过贡献代码，你同意你的贡献将在与项目相同的MIT许可证下发布。

---

## 联系方式

- **Issues**: https://github.com/TerryLiang9/daily-learning-hello-agnet/issues
- **Discussions**: https://github.com/TerryLiang9/daily-learning-hello-agnet/discussions
- **Email**: your-email@example.com

---

## 致谢

感谢所有贡献者！

<!-- 这里的贡献者列表将通过GitHub Actions自动更新 -->
<a href="https://github.com/TerryLiang9/daily-learning-hello-agnet/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=TerryLiang9/daily-learning-hello-agnet" />
</a>

---

**再次感谢你的贡献！** 🎉

让我们一起构建更好的智能体学习社区！

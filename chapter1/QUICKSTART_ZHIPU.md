# 🚀 智谱 AI 快速配置指南

本文档介绍如何使用智谱 AI（BigModel）运行智能旅行助手。

## 📝 步骤 1：获取智谱 API Key

1. 访问 [智谱 AI 开放平台](https://open.bigmodel.cn/)
2. 注册/登录账号
3. 进入 [API Keys 页面](https://open.bigmodel.cn/usercenter/apikeys)
4. 创建新的 API Key（格式：`xxxxxxxxxxxxxxxx.xxxxxxxxxxxxxx`）
5. 复制 API Key

**💰 新用户福利：**
- 免费赠送 25 元额度
- `glm-4-flash` 模型完全免费
- 足够完成本教程所有练习

---

## ⚙️ 步骤 2：配置环境变量

### 方式 A：使用配置文件（推荐）

```bash
# 复制配置模板
cp .env.example .env
```

编辑 `.env` 文件：

```env
# 智谱 AI 配置
API_KEY=你的智谱API_Key
BASE_URL=https://open.bigmodel.cn/api/anthropic
MODEL_ID=glm-4-flash

# Tavily 搜索 API
TAVILY_API_KEY=你的Tavily_API_Key
```

### 方式 B：直接设置环境变量（临时测试）

**Windows (PowerShell):**
```powershell
$env:API_KEY="你的智谱API_Key"
$env:BASE_URL="https://open.bigmodel.cn/api/anthropic"
$env:MODEL_ID="glm-4-flash"
$env:TAVILY_API_KEY="你的Tavily_API_Key"

python agent.py
```

**Windows (CMD):**
```cmd
set API_KEY=你的智谱API_Key
set BASE_URL=https://open.bigmodel.cn/api/anthropic
set MODEL_ID=glm-4-flash
set TAVILY_API_KEY=你的Tavily_API_Key

python agent.py
```

**Linux/Mac:**
```bash
export API_KEY="你的智谱API_Key"
export BASE_URL="https://open.bigmodel.cn/api/anthropic"
export MODEL_ID="glm-4-flash"
export TAVILY_API_KEY="你的Tavily_API_Key"

python agent.py
```

---

## 🤖 步骤 3：运行智能体

```bash
# 运行默认任务
python agent.py

# 交互式对话
python agent.py --interactive
```

---

## 🔧 智谱 AI 可用模型

| 模型名称 | 说明 | 价格 |
|---------|------|------|
| `glm-4-flash` | 速度最快，完全免费 | 免费 ⭐ |
| `glm-4-air` | 轻量级，性价比高 | ¥0.1/千tokens |
| `glm-4-plus` | 性能最强 | ¥0.5/千tokens |
| `glm-4.7` | 平衡型 | ¥0.5/千tokens |

**学习建议：** 使用 `glm-4-flash` 完全足够，速度快且免费！

---

## ❓ 常见问题

### Q1: 提示 "API Key 格式错误"

**A:** 智谱 AI 的 API Key 格式为 `id.secret`，确保复制完整的 Key。

### Q2: 提示 "模型不存在"

**A:** 检查 `MODEL_ID` 是否正确，推荐使用 `glm-4-flash`。

### Q3: 连接超时

**A:** 可能是网络问题，尝试：
1. 检查网络连接
2. 确认 `BASE_URL` 设置正确
3. 如果使用代理，确保代理配置正确

### Q4: 额度不足

**A:** 访问 [智谱控制台](https://open.bigmodel.cn/usercenter/balance) 查看余额，新用户有 25 元免费额度。

---

## 📚 更多资源

- [智谱 AI 官方文档](https://open.bigmodel.cn/dev/api)
- [模型定价](https://open.bigmodel.cn/pricing)
- [SDK 使用指南](https://github.com/THUDM/ChatGLM)

---

**配置完成后，回到 [README.md](./README.md) 继续学习！** 🎉

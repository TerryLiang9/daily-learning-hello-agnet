# 第十一章：Agentic-RL

> 从SFT到GRPO的LLM训练实战

**本章重点**：
- 理解强化学习在智能体训练中的应用
- 掌握SFT、GRPO等训练方法
- 实践：训练一个优化的智能体

---

## 学习笔记

### 11.1 为什么需要强化学习？

**传统监督学习的局限**：
1. 依赖标注数据，成本高
2. 难以优化长期目标
3. 无法从交互中学习

**强化学习的优势**：
1. 从反馈中学习
2. 优化长期回报
3. 适应动态环境

### 11.2 训练方法演进

```
LLM训练方法演进
├── Pre-training (预训练)
├── SFT (Supervised Fine-Tuning)
├── RLHF (Reinforcement Learning from Human Feedback)
└── GRPO (Group Relative Policy Optimization)
```

| 方法 | 原理 | 优势 | 局限 |
|------|------|------|------|
| **SFT** | 监督微调 | 稳定、可控 | 需要标注数据 |
| **RLHF** | 人类反馈强化学习 | 对齐人类偏好 | 成本高、不稳定 |
| **GRPO** | 群体相对策略优化 | 稳定、高效 | 实现复杂 |

---

## 实现代码

### 1. 奖励模型

```python
# reward_model.py

from typing import List, Dict
import torch
import torch.nn as nn


class RewardModel(nn.Module):
    """奖励模型"""

    def __init__(self, base_model: nn.Module, hidden_size: int = 768):
        super().__init__()
        self.base_model = base_model
        self.reward_head = nn.Sequential(
            nn.Linear(hidden_size, 512),
            nn.ReLU(),
            nn.Dropout(0.1),
            nn.Linear(512, 1),
            nn.Tanh()  # 输出范围[-1, 1]
        )

    def forward(self, input_ids, attention_mask):
        """前向传播"""
        # 获取base model的输出
        outputs = self.base_model(
            input_ids=input_ids,
            attention_mask=attention_mask
        )

        # 使用[CLS] token的表示
        hidden_state = outputs.last_hidden_state[:, 0, :]

        # 计算奖励
        reward = self.reward_head(hidden_state)
        return reward


class PreferenceDataset:
    """偏好数据集"""

    def __init__(self):
        self.pairs = []

    def add_pair(self, chosen: str, rejected: str):
        """添加偏好对"""
        self.pairs.append({
            "chosen": chosen,
            "rejected": rejected
        })

    def get_batch(self, batch_size: int) -> List[Dict]:
        """获取批次数据"""
        import random
        return random.sample(self.pairs, min(batch_size, len(self.pairs)))


# 使用示例
if __name__ == "__main__":
    # 创建模拟数据
    dataset = PreferenceDataset()
    dataset.add_pair(
        chosen="这是一个很好的回答，详细且准确。",
        rejected="这个回答太简短了，信息不足。"
    )
    dataset.add_pair(
        chosen="代码实现正确，有详细注释。",
        rejected="代码有bug，没有注释。"
    )

    # 获取批次
    batch = dataset.get_batch(2)
    print(f"批次数据: {batch}")
```

### 2. GRPO训练实现

```python
# grpo_trainer.py

from typing import List, Dict, Optional
import torch
import torch.nn as nn
from torch.optim import Adam
from reward_model import RewardModel


class GRPOTrainer:
    """GRPO训练器"""

    def __init__(self,
                 policy_model: nn.Module,
                 reward_model: RewardModel,
                 learning_rate: float = 1e-5):
        self.policy_model = policy_model
        self.reward_model = reward_model
        self.optimizer = Adam(policy_model.parameters(), lr=learning_rate)

        self.clip_ratio = 0.2  # PPO裁剪比率
        self.kl_coef = 0.1  # KL散度系数

    def generate_responses(self,
                          prompts: List[str],
                          num_responses: int = 4) -> List[List[str]]:
        """生成多个响应（群体采样）"""
        all_responses = []

        for prompt in prompts:
            responses = []
            for _ in range(num_responses):
                # 生成响应
                response = self._generate(prompt)
                responses.append(response)
            all_responses.append(responses)

        return all_responses

    def _generate(self, prompt: str) -> str:
        """生成单个响应（简化实现）"""
        # 实际应用中应该使用真实的生成模型
        return f"基于'{prompt}'的响应"

    def compute_rewards(self,
                       prompts: List[str],
                       response_groups: List[List[str]]) -> List[List[float]]:
        """计算奖励"""
        all_rewards = []

        for prompt, responses in zip(prompts, response_groups):
            group_rewards = []
            for response in responses:
                # 计算奖励分数
                reward = self._compute_single_reward(prompt, response)
                group_rewards.append(reward)
            all_rewards.append(group_rewards)

        return all_rewards

    def _compute_single_reward(self, prompt: str, response: str) -> float:
        """计算单个奖励（简化实现）"""
        # 实际应用中应该使用reward model
        # 这里使用简单的规则
        if len(response) > 10 and "详细" in response:
            return 0.8
        elif len(response) > 5:
            return 0.5
        else:
            return 0.2

    def compute_group advantages(self, reward_groups: List[List[float]]) -> List[List[float]]:
        """计算群体优势（Group Relative Advantages）"""
        advantage_groups = []

        for rewards in reward_groups:
            # 计算组内平均奖励
            mean_reward = sum(rewards) / len(rewards)

            # 计算相对优势
            advantages = [r - mean_reward for r in rewards]
            advantage_groups.append(advantages)

        return advantage_groups

    def update_policy(self,
                     prompts: List[str],
                     response_groups: List[List[str]],
                     advantage_groups: List[List[float]]):
        """更新策略"""
        total_loss = 0

        for prompt, responses, advantages in zip(prompts, response_groups, advantage_groups):
            for response, advantage in zip(responses, advantages):
                # 计算策略损失
                loss = self._compute_policy_loss(prompt, response, advantage)

                # 反向传播
                self.optimizer.zero_grad()
                loss.backward()
                self.optimizer.step()

                total_loss += loss.item()

        avg_loss = total_loss / sum(len(g) for g in response_groups)
        return avg_loss

    def _compute_policy_loss(self, prompt: str, response: str, advantage: float) -> torch.Tensor:
        """计算策略损失（简化实现）"""
        # 实际应用中应该计算log概率和KL散度
        policy_loss = -advantage  # 简化实现
        return torch.tensor(policy_loss, requires_grad=True)

    def train_step(self, prompts: List[str]) -> Dict[str, float]:
        """执行一步训练"""
        # 1. 生成响应
        response_groups = self.generate_responses(prompts, num_responses=4)

        # 2. 计算奖励
        reward_groups = self.compute_rewards(prompts, response_groups)

        # 3. 计算优势
        advantage_groups = self.compute_group_advantages(reward_groups)

        # 4. 更新策略
        avg_loss = self.update_policy(prompts, response_groups, advantage_groups)

        # 5. 统计
        avg_reward = sum(sum(g) for g in reward_groups) / sum(len(g) for g in reward_groups)

        return {
            "loss": avg_loss,
            "avg_reward": avg_reward
        }

    def train(self,
              prompts: List[str],
              num_steps: int = 100):
        """训练循环"""
        print("开始GRPO训练...")

        for step in range(num_steps):
            # 执行训练步骤
            metrics = self.train_step(prompts)

            # 打印进度
            if step % 10 == 0:
                print(f"Step {step}: Loss={metrics['loss']:.4f}, Reward={metrics['avg_reward']:.4f}")

        print("训练完成！")


# 使用示例
if __name__ == "__main__":
    import torch.nn as nn

    # 创建模拟模型
    class DummyModel(nn.Module):
        def __init__(self):
            super().__init__()
            self.linear = nn.Linear(10, 1)

    policy_model = DummyModel()
    base_model = DummyModel()
    reward_model = RewardModel(base_model)

    # 创建训练器
    trainer = GRPOTrainer(policy_model, reward_model)

    # 训练数据
    prompts = [
        "解释什么是机器学习",
        "如何使用Python进行数据分析",
        "什么是深度学习"
    ]

    # 训练
    trainer.train(prompts, num_steps=20)
```

---

## 学习总结

### 核心概念

1. **奖励建模**：学习人类偏好
2. **群体采样**：生成多个候选响应
3. **相对优势**：比较组内响应
4. **策略优化**：提升高质量响应概率

### GRPO vs RLHF

| 特性 | RLHF | GRPO |
|------|------|------|
| 稳定性 | 较低 | 更高 |
| 样本效率 | 中等 | 更高 |
| 实现难度 | 复杂 | 中等 |
| 训练成本 | 高 | 相对较低 |

---

## 参考资源

- [DeepSeek GRPO论文](https://arxiv.org/abs/2406.01706)
- [RLHF原始论文](https://arxiv.org/abs/2203.02155)
- [PPO算法详解](https://arxiv.org/abs/1707.06347)

---

## 许可证

MIT License

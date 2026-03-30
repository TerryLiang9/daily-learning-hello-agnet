"""
记忆模块
用于存储智能体的行动与反思轨迹
"""

from typing import List, Dict, Any, Optional


class Memory:
  """
  一个简单的短期记忆模块，用于存储智能体的行动与反思轨迹。
  """

  def __init__(self):
    """
    初始化一个空列表来存储所有记录。
    """
    self.records: List[Dict[str, Any]] = []

  def add_record(self, record_type: str, content: str):
    """
    向记忆中添加一条新记录。

    参数:
    - record_type (str): 记录的类型 ('execution' 或 'reflection')。
    - content (str): 记录的具体内容 (例如，生成的代码或反思的反馈)。
    """
    record = {"type": record_type, "content": content}
    self.records.append(record)
    print(f"📝 记忆已更新，新增一条 '{record_type}' 记录。")

  def get_trajectory(self) -> str:
    """
    将所有记忆记录格式化为一个连贯的字符串文本，用于构建提示词。
    """
    trajectory_parts = []
    for record in self.records:
      if record['type'] == 'execution':
        trajectory_parts.append(
          f"--- 上一轮尝试 (代码) ---\n{record['content']}")
      elif record['type'] == 'reflection':
        trajectory_parts.append(f"--- 评审员反馈 ---\n{record['content']}")

    return "\n\n".join(trajectory_parts)

  def get_last_execution(self) -> Optional[str]:
    """
    获取最近一次的执行结果 (例如，最新生成的代码)。
    如果不存在，则返回 None。
    """
    for record in reversed(self.records):
      if record['type'] == 'execution':
        return record['content']
    return None


# --- 记忆模块使用示例 ---
if __name__ == '__main__':
  memory = Memory()

  # 添加执行记录
  memory.add_record("execution", "def hello():\n    print('Hello World')")

  # 添加反思记录
  memory.add_record("reflection", "代码缺少文档字符串，需要添加")

  # 获取轨迹
  print("\n--- 完整轨迹 ---")
  print(memory.get_trajectory())

  # 获取最后一次执行
  print("\n--- 最后一次执行 ---")
  print(memory.get_last_execution())

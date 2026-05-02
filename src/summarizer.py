"""
摘要生成模块
使用 Claude API 生成文章摘要
"""

from anthropic import Anthropic
import config


class Summarizer:
    """摘要生成器"""

    def __init__(self, api_key: str = None):
        """
        初始化摘要生成器

        Args:
            api_key: Claude API Key
        """
        self.api_key = api_key or config.CLAUDE_API_KEY
        if not self.api_key:
            raise ValueError("请设置 CLAUDE_API_KEY 环境变量")

        self.client = Anthropic(api_key=self.api_key)
        self.model = config.MODEL

    def summarize(self, text: str) -> str:
        """
        生成文章摘要

        Args:
            text: 文章内容

        Returns:
            摘要文本
        """
        prompt = config.SUMMARY_PROMPT.format(text=text)

        message = self.client.messages.create(
            model=self.model,
            max_tokens=4096,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        return message.content[0].text

    def extract_key_points(self, text: str) -> list:
        """
        提取关键要点

        Args:
            text: 文章内容

        Returns:
            关键要点列表
        """
        prompt = f"""请从以下文章中提取5-10个关键要点，每个要点用一句话概括：

{text}

请以列表形式输出，每行一个要点。"""

        message = self.client.messages.create(
            model=self.model,
            max_tokens=2048,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        # 解析返回的要点
        response = message.content[0].text
        points = [line.strip() for line in response.split('\n') if line.strip()]

        return points

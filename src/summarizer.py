"""
摘要生成模块
支持 Anthropic 和智谱 API
"""

import config


class Summarizer:
    """摘要生成器"""

    def __init__(self, api_key: str = None):
        """
        初始化摘要生成器

        Args:
            api_key: API Key
        """
        self.api_key = api_key or config.API_KEY
        if not self.api_key:
            raise ValueError("请设置 API Key 环境变量")

        # 根据 API 类型初始化客户端
        if config.USE_OPENAI_FORMAT:
            from openai import OpenAI
            self.client = OpenAI(
                api_key=self.api_key,
                base_url=config.BASE_URL
            )
        else:
            from anthropic import Anthropic
            self.client = Anthropic(
                api_key=self.api_key,
                base_url=config.BASE_URL
            )

        self.model = config.MODEL
        self.use_openai_format = config.USE_OPENAI_FORMAT

    def summarize(self, text: str) -> str:
        """
        生成文章摘要

        Args:
            text: 文章内容

        Returns:
            摘要文本
        """
        prompt = config.SUMMARY_PROMPT.format(text=text)

        if self.use_openai_format:
            # 智谱 API（OpenAI 格式）
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=4096,
                temperature=0.7
            )
            return response.choices[0].message.content
        else:
            # Anthropic API
            message = self.client.messages.create(
                model=self.model,
                max_tokens=4096,
                messages=[{"role": "user", "content": prompt}]
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

        if self.use_openai_format:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=2048,
                temperature=0.7
            )
            content = response.choices[0].message.content
        else:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=2048,
                messages=[{"role": "user", "content": prompt}]
            )
            content = message.content[0].text

        # 解析返回的要点
        points = [line.strip() for line in content.split('\n') if line.strip()]
        return points

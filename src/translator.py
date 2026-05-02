"""
翻译模块
使用 Claude API 进行智能翻译
"""

from anthropic import Anthropic
import config


class Translator:
    """翻译器"""

    def __init__(self, api_key: str = None):
        """
        初始化翻译器

        Args:
            api_key: Claude API Key，如果不提供则从配置文件读取
        """
        self.api_key = api_key or config.CLAUDE_API_KEY
        if not self.api_key:
            raise ValueError("请设置 CLAUDE_API_KEY 环境变量")

        self.client = Anthropic(api_key=self.api_key)
        self.model = config.MODEL

    def translate(self, text: str, chunk_size: int = 3000) -> str:
        """
        翻译英文文本为中文

        Args:
            text: 英文文本
            chunk_size: 分块大小（字符数），用于处理长文本

        Returns:
            翻译后的中文文本
        """
        # 如果文本较短，直接翻译
        if len(text) <= chunk_size:
            return self._translate_chunk(text)

        # 长文本分块处理
        chunks = self._split_text(text, chunk_size)
        translated_chunks = []

        for i, chunk in enumerate(chunks):
            print(f"正在翻译第 {i + 1}/{len(chunks)} 部分...")
            translated = self._translate_chunk(chunk)
            translated_chunks.append(translated)

        return "\n\n".join(translated_chunks)

    def _translate_chunk(self, text: str) -> str:
        """翻译单个文本块"""
        prompt = config.TRANSLATION_PROMPT.format(text=text)

        message = self.client.messages.create(
            model=self.model,
            max_tokens=4096,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        return message.content[0].text

    def _split_text(self, text: str, chunk_size: int) -> list:
        """
        将长文本分块

        Args:
            text: 原文本
            chunk_size: 每块的大小

        Returns:
            文本块列表
        """
        # 按段落分割
        paragraphs = text.split('\n\n')
        chunks = []
        current_chunk = ""

        for para in paragraphs:
            if len(current_chunk) + len(para) <= chunk_size:
                current_chunk += para + "\n\n"
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = para + "\n\n"

        if current_chunk:
            chunks.append(current_chunk.strip())

        return chunks

"""
笔记生成模块
支持 Anthropic 和智谱 API
"""

import config
from datetime import datetime
from pathlib import Path


class NoteGenerator:
    """笔记生成器"""

    def __init__(self, api_key: str = None):
        """
        初始化笔记生成器

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

    def generate_note(self, text: str, title: str = None) -> str:
        """
        生成学习笔记

        Args:
            text: 文章内容
            title: 笔记标题

        Returns:
            Markdown 格式的笔记
        """
        prompt = config.NOTE_PROMPT.format(text=text)

        if self.use_openai_format:
            # 智谱 API（OpenAI 格式）
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=4096,
                temperature=0.7
            )
            note_content = response.choices[0].message.content
        else:
            # Anthropic API
            message = self.client.messages.create(
                model=self.model,
                max_tokens=4096,
                messages=[{"role": "user", "content": prompt}]
            )
            note_content = message.content[0].text

        # 添加元数据
        metadata = self._generate_metadata(title)
        full_note = f"{metadata}\n\n{note_content}"

        return full_note

    def save_note(self, note_content: str, filename: str = None) -> str:
        """
        保存笔记到文件

        Args:
            note_content: 笔记内容
            filename: 文件名（不含路径）

        Returns:
            保存的文件路径
        """
        output_dir = Path(config.OUTPUT_DIR)
        output_dir.mkdir(parents=True, exist_ok=True)

        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"note_{timestamp}.md"

        if not filename.endswith('.md'):
            filename += '.md'

        file_path = output_dir / filename
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(note_content)

        return str(file_path)

    def _generate_metadata(self, title: str = None) -> str:
        """生成笔记元数据"""
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        title = title or "英文阅读笔记"

        metadata = f"""---
title: {title}
date: {now}
tags: [英文阅读, 学习笔记]
---
"""
        return metadata

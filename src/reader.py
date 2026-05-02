"""
文件读取模块
支持多种格式：txt, md, pdf
"""

import os
from pathlib import Path


class FileReader:
    """文件读取器"""

    def __init__(self):
        self.supported_formats = ['.txt', '.md', '.pdf']

    def read_file(self, file_path: str) -> str:
        """
        读取文件内容

        Args:
            file_path: 文件路径

        Returns:
            文件内容（字符串）
        """
        file_path = Path(file_path)

        if not file_path.exists():
            raise FileNotFoundError(f"文件不存在: {file_path}")

        suffix = file_path.suffix.lower()

        if suffix not in self.supported_formats:
            raise ValueError(f"不支持的文件格式: {suffix}")

        if suffix in ['.txt', '.md']:
            return self._read_text_file(file_path)
        elif suffix == '.pdf':
            return self._read_pdf_file(file_path)

    def _read_text_file(self, file_path: Path) -> str:
        """读取文本文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except UnicodeDecodeError:
            # 尝试其他编码
            with open(file_path, 'r', encoding='gbk') as f:
                return f.read()

    def _read_pdf_file(self, file_path: Path) -> str:
        """读取 PDF 文件"""
        try:
            import pdfplumber

            text = ""
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() + "\n\n"

            return text.strip()
        except ImportError:
            # 如果 pdfplumber 不可用，尝试 PyPDF2
            import PyPDF2

            text = ""
            with open(file_path, 'rb') as f:
                pdf_reader = PyPDF2.PdfReader(f)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n\n"

            return text.strip()

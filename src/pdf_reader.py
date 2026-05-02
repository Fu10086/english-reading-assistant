"""
PDF 文件解析模块
支持多种 PDF 解析方法
"""

import pdfplumber
from pathlib import Path
from typing import Optional


class PDFReader:
    """PDF 文件读取器"""

    def __init__(self):
        pass

    def read_pdf(self, file_path: str, method: str = "pdfplumber") -> str:
        """
        读取 PDF 文件内容

        Args:
            file_path: PDF 文件路径
            method: 解析方法 (pdfplumber/pypdf2)

        Returns:
            提取的文本内容
        """
        file_path = Path(file_path)

        if not file_path.exists():
            raise FileNotFoundError(f"文件不存在: {file_path}")

        if not file_path.suffix.lower() == '.pdf':
            raise ValueError(f"不是 PDF 文件: {file_path}")

        if method == "pdfplumber":
            return self._read_with_pdfplumber(file_path)
        elif method == "pypdf2":
            return self._read_with_pypdf2(file_path)
        else:
            raise ValueError(f"未知的解析方法: {method}")

    def _read_with_pdfplumber(self, file_path: Path) -> str:
        """使用 pdfplumber 读取 PDF（推荐，效果更好）"""
        text_parts = []

        try:
            with pdfplumber.open(file_path) as pdf:
                total_pages = len(pdf.pages)

                for i, page in enumerate(pdf.pages, 1):
                    # 提取文本
                    text = page.extract_text()

                    if text:
                        text_parts.append(f"--- Page {i}/{total_pages} ---\n")
                        text_parts.append(text)
                        text_parts.append("\n\n")

                if not text_parts:
                    raise ValueError("PDF 中没有提取到文本内容")

                return "".join(text_parts)

        except Exception as e:
            raise Exception(f"PDF 解析失败: {str(e)}")

    def _read_with_pypdf2(self, file_path: Path) -> str:
        """使用 PyPDF2 读取 PDF（备用方法）"""
        from PyPDF2 import PdfReader

        text_parts = []

        try:
            reader = PdfReader(file_path)
            total_pages = len(reader.pages)

            for i, page in enumerate(reader.pages, 1):
                text = page.extract_text()

                if text:
                    text_parts.append(f"--- Page {i}/{total_pages} ---\n")
                    text_parts.append(text)
                    text_parts.append("\n\n")

            if not text_parts:
                raise ValueError("PDF 中没有提取到文本内容")

            return "".join(text_parts)

        except Exception as e:
            raise Exception(f"PDF 解析失败: {str(e)}")

    def get_pdf_info(self, file_path: str) -> dict:
        """
        获取 PDF 文件信息

        Args:
            file_path: PDF 文件路径

        Returns:
            PDF 信息字典
        """
        file_path = Path(file_path)

        try:
            with pdfplumber.open(file_path) as pdf:
                info = {
                    "pages": len(pdf.pages),
                    "metadata": pdf.metadata,
                }

                # 估算字符数
                total_chars = 0
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        total_chars += len(text)

                info["estimated_chars"] = total_chars

                return info

        except Exception as e:
            return {"error": str(e)}


def test_pdf_reader():
    """测试 PDF 读取功能"""
    reader = PDFReader()

    # 测试文件
    test_file = "test.pdf"

    if Path(test_file).exists():
        print(f"测试读取: {test_file}")

        # 获取信息
        info = reader.get_pdf_info(test_file)
        print(f"页数: {info.get('pages')}")
        print(f"字符数: {info.get('estimated_chars')}")

        # 读取内容
        content = reader.read_pdf(test_file)
        print(f"\n前 500 字符:")
        print(content[:500])
    else:
        print(f"测试文件不存在: {test_file}")
        print("请提供一个 PDF 文件进行测试")


if __name__ == "__main__":
    test_pdf_reader()

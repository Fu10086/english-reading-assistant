#!/usr/bin/env python3
"""
English Reading Assistant - 主程序
"""

import argparse
import sys
from pathlib import Path

# 添加 src 目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from src.reader import FileReader
from src.translator import Translator
from src.summarizer import Summarizer
from src.note_generator import NoteGenerator
from src.qa_agent import QAAgent


def main():
    parser = argparse.ArgumentParser(
        description="English Reading Assistant - AI驱动的英文阅读助手"
    )
    parser.add_argument(
        "--file", "-f",
        required=True,
        help="输入文件路径（支持 .txt, .md, .pdf）"
    )
    parser.add_argument(
        "--mode", "-m",
        choices=["translate", "summary", "note", "full", "qa"],
        default="full",
        help="处理模式：translate(翻译), summary(摘要), note(笔记), full(完整分析), qa(问答)"
    )
    parser.add_argument(
        "--output", "-o",
        help="输出文件路径（可选）"
    )
    parser.add_argument(
        "--interactive", "-i",
        action="store_true",
        help="交互式问答模式"
    )

    args = parser.parse_args()

    try:
        # 1. 读取文件
        print(f"正在读取文件: {args.file}")
        reader = FileReader()
        content = reader.read_file(args.file)
        print(f"文件读取成功，共 {len(content)} 字符\n")

        # 2. 根据模式处理
        if args.mode == "translate":
            print("=== 翻译模式 ===\n")
            translator = Translator()
            result = translator.translate(content)
            print(result)

        elif args.mode == "summary":
            print("=== 摘要模式 ===\n")
            summarizer = Summarizer()
            result = summarizer.summarize(content)
            print(result)

        elif args.mode == "note":
            print("=== 笔记生成模式 ===\n")
            note_gen = NoteGenerator()
            filename = Path(args.file).stem
            result = note_gen.generate_note(content, title=filename)

            # 保存笔记
            output_path = note_gen.save_note(result, filename=f"{filename}_note")
            print(f"笔记已保存到: {output_path}\n")
            print(result)

        elif args.mode == "full":
            print("=== 完整分析模式 ===\n")

            # 翻译
            print("1. 正在翻译...")
            translator = Translator()
            translation = translator.translate(content)

            # 摘要
            print("\n2. 正在生成摘要...")
            summarizer = Summarizer()
            summary = summarizer.summarize(content)

            # 生成笔记
            print("\n3. 正在生成笔记...")
            note_gen = NoteGenerator()
            filename = Path(args.file).stem

            full_note = f"""# {filename}

## 摘要

{summary}

---

## 翻译

{translation}
"""

            output_path = note_gen.save_note(full_note, filename=f"{filename}_full")
            print(f"\n完整笔记已保存到: {output_path}")

        elif args.mode == "qa" or args.interactive:
            print("=== 问答模式 ===\n")
            qa = QAAgent()
            qa.set_context(content)

            if args.interactive:
                qa.interactive_mode()
            else:
                print("请使用 --interactive 参数进入交互式问答")

    except FileNotFoundError as e:
        print(f"错误: {e}")
        sys.exit(1)
    except ValueError as e:
        print(f"错误: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"发生错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

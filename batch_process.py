"""
批量处理工具
一次处理多个文件
"""

import os
from pathlib import Path
from datetime import datetime
import json

from src.translator import Translator
from src.summarizer import Summarizer
from src.note_generator import NoteGenerator
from src.reader import FileReader


def batch_process(input_dir: str, mode: str = "summary", output_dir: str = None):
    """
    批量处理文件

    Args:
        input_dir: 输入目录
        mode: 处理模式 (summary/translate/note/full)
        output_dir: 输出目录
    """
    input_path = Path(input_dir)
    if not input_path.exists():
        print(f"❌ 目录不存在: {input_dir}")
        return

    # 获取所有文本文件
    files = list(input_path.glob("*.txt")) + list(input_path.glob("*.md"))

    if not files:
        print(f"❌ 目录中没有找到文本文件: {input_dir}")
        return

    print(f"\n📁 找到 {len(files)} 个文件")
    print("="*60)

    # 初始化处理器
    reader = FileReader()
    results = []

    for i, file_path in enumerate(files, 1):
        print(f"\n[{i}/{len(files)}] 处理: {file_path.name}")
        print("-"*60)

        try:
            # 读取文件
            content = reader.read_file(str(file_path))
            print(f"✅ 读取成功，共 {len(content)} 字符")

            # 根据模式处理
            if mode == "summary":
                print("⏳ 生成摘要...")
                summarizer = Summarizer()
                result = summarizer.summarize(content)
                output_file = f"summary_{file_path.stem}.md"

            elif mode == "translate":
                print("⏳ 翻译中...")
                translator = Translator()
                result = translator.translate(content)
                output_file = f"translation_{file_path.stem}.md"

            elif mode == "note":
                print("⏳ 生成笔记...")
                note_gen = NoteGenerator()
                result = note_gen.generate_note(content, title=file_path.stem)
                output_file = f"note_{file_path.stem}.md"

            elif mode == "full":
                print("⏳ 完整分析...")
                translator = Translator()
                summarizer = Summarizer()
                note_gen = NoteGenerator()

                translation = translator.translate(content)
                summary = summarizer.summarize(content)
                note = note_gen.generate_note(content, title=file_path.stem)

                result = f"# {file_path.stem}\n\n## 摘要\n\n{summary}\n\n## 翻译\n\n{translation}\n\n## 笔记\n\n{note}"
                output_file = f"full_{file_path.stem}.md"

            else:
                print(f"❌ 未知模式: {mode}")
                continue

            # 保存结果
            if output_dir:
                output_path = Path(output_dir)
            else:
                output_path = Path("data/output/batch")

            output_path.mkdir(parents=True, exist_ok=True)

            with open(output_path / output_file, 'w', encoding='utf-8') as f:
                f.write(result)

            print(f"✅ 已保存: {output_path / output_file}")

            results.append({
                "file": file_path.name,
                "status": "success",
                "output": str(output_path / output_file),
                "chars": len(content)
            })

        except Exception as e:
            print(f"❌ 处理失败: {e}")
            results.append({
                "file": file_path.name,
                "status": "failed",
                "error": str(e)
            })

    # 生成报告
    print("\n" + "="*60)
    print("📊 批量处理完成")
    print("="*60)

    success_count = sum(1 for r in results if r["status"] == "success")
    failed_count = len(results) - success_count

    print(f"\n✅ 成功: {success_count} 个")
    print(f"❌ 失败: {failed_count} 个")

    # 保存报告
    report_path = Path("data/output/batch") / f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    report_path.parent.mkdir(parents=True, exist_ok=True)

    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "mode": mode,
            "total": len(files),
            "success": success_count,
            "failed": failed_count,
            "results": results
        }, f, indent=2, ensure_ascii=False)

    print(f"\n📄 报告已保存: {report_path}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("用法: python batch_process.py <输入目录> [模式] [输出目录]")
        print("模式: summary (默认) | translate | note | full")
        print("\n示例:")
        print("  python batch_process.py data/input")
        print("  python batch_process.py data/input summary")
        print("  python batch_process.py data/input full data/output/my_batch")
        sys.exit(1)

    input_dir = sys.argv[1]
    mode = sys.argv[2] if len(sys.argv) > 2 else "summary"
    output_dir = sys.argv[3] if len(sys.argv) > 3 else None

    batch_process(input_dir, mode, output_dir)

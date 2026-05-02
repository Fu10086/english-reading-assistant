"""
英文阅读助手 - 本地简化版
直接在命令行运行，带简单交互
"""

import os
from pathlib import Path

# 导入核心模块
from src.translator import Translator
from src.summarizer import Summarizer
from src.note_generator import NoteGenerator
from src.qa_agent import QAAgent
from src.reader import FileReader

def print_header():
    print("\n" + "="*60)
    print("📚 英文阅读助手 - 交互式版本")
    print("="*60 + "\n")

def print_menu():
    print("\n请选择功能：")
    print("1. 📋 生成摘要（最快）")
    print("2. 🌐 翻译文章")
    print("3. 📝 生成笔记")
    print("4. 🎯 完整分析（翻译+摘要+笔记）")
    print("5. 💬 问答模式")
    print("0. 退出")
    print("-" * 60)

def get_input_text():
    print("\n请选择输入方式：")
    print("1. 输入文件路径")
    print("2. 粘贴文本内容")
    choice = input("选择 (1/2): ").strip()

    if choice == "1":
        file_path = input("请输入文件路径: ").strip()
        try:
            reader = FileReader()
            content = reader.read_file(file_path)
            print(f"✅ 文件读取成功，共 {len(content)} 字符")
            return content
        except Exception as e:
            print(f"❌ 读取失败: {e}")
            return None
    elif choice == "2":
        print("请粘贴文本内容（输入 END 结束）：")
        lines = []
        while True:
            line = input()
            if line.strip() == "END":
                break
            lines.append(line)
        content = "\n".join(lines)
        print(f"✅ 文本输入完成，共 {len(content)} 字符")
        return content
    else:
        print("❌ 无效选择")
        return None

def main():
    print_header()

    while True:
        print_menu()
        choice = input("请选择功能 (0-5): ").strip()

        if choice == "0":
            print("\n👋 再见！")
            break

        if choice not in ["1", "2", "3", "4", "5"]:
            print("❌ 无效选择，请重新输入")
            continue

        # 获取输入内容
        content = get_input_text()
        if not content:
            continue

        try:
            if choice == "1":
                # 摘要
                print("\n⏳ 正在生成摘要...")
                summarizer = Summarizer()
                result = summarizer.summarize(content)
                print("\n" + "="*60)
                print("📋 摘要结果")
                print("="*60)
                print(result)

                # 保存选项
                save = input("\n是否保存到文件？(y/n): ").strip().lower()
                if save == 'y':
                    filename = f"summary_{Path().absolute().name}.md"
                    with open(f"data/output/{filename}", 'w', encoding='utf-8') as f:
                        f.write(result)
                    print(f"✅ 已保存到: data/output/{filename}")

            elif choice == "2":
                # 翻译
                print("\n⏳ 正在翻译...")
                translator = Translator()
                result = translator.translate(content)
                print("\n" + "="*60)
                print("🌐 翻译结果")
                print("="*60)
                print(result)

                save = input("\n是否保存到文件？(y/n): ").strip().lower()
                if save == 'y':
                    filename = f"translation_{Path().absolute().name}.md"
                    with open(f"data/output/{filename}", 'w', encoding='utf-8') as f:
                        f.write(result)
                    print(f"✅ 已保存到: data/output/{filename}")

            elif choice == "3":
                # 笔记
                print("\n⏳ 正在生成笔记...")
                note_gen = NoteGenerator()
                result = note_gen.generate_note(content)
                saved_path = note_gen.save_note(result)
                print("\n" + "="*60)
                print("📝 学习笔记")
                print("="*60)
                print(result)
                print(f"\n✅ 已自动保存到: {saved_path}")

            elif choice == "4":
                # 完整分析
                print("\n⏳ 正在进行完整分析...")

                print("  [1/3] 正在翻译...")
                translator = Translator()
                translation = translator.translate(content)

                print("  [2/3] 正在生成摘要...")
                summarizer = Summarizer()
                summary = summarizer.summarize(content)

                print("  [3/3] 正在生成笔记...")
                note_gen = NoteGenerator()
                note = note_gen.generate_note(content)
                saved_path = note_gen.save_note(note)

                print("\n" + "="*60)
                print("🎯 完整分析结果")
                print("="*60)

                print("\n📋 摘要：")
                print("-" * 60)
                print(summary)

                print("\n🌐 翻译：")
                print("-" * 60)
                print(translation[:500] + "..." if len(translation) > 500 else translation)

                print(f"\n✅ 完整笔记已保存到: {saved_path}")

            elif choice == "5":
                # 问答模式
                print("\n💬 进入问答模式")
                print("提示：输入 'quit' 或 'exit' 退出问答模式\n")

                qa_agent = QAAgent()
                qa_agent.set_context(content)

                while True:
                    question = input("\n你的问题: ").strip()

                    if question.lower() in ['quit', 'exit', 'q']:
                        print("退出问答模式")
                        break

                    if not question:
                        continue

                    print("\n💡 回答:")
                    answer = qa_agent.ask(question)
                    print(answer)
                    print("-" * 60)

        except Exception as e:
            print(f"\n❌ 处理失败: {e}")
            import traceback
            traceback.print_exc()

        input("\n按 Enter 继续...")

if __name__ == "__main__":
    main()

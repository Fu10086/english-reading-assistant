"""
简单问答工具 - 直接在命令行使用
"""

from src.qa_agent import QAAgent
from src.reader import FileReader
import sys

def main():
    print("\n" + "="*60)
    print("💬 英文阅读助手 - 问答模式")
    print("="*60 + "\n")

    # 获取文件路径
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    else:
        file_path = input("请输入文件路径: ").strip()

    # 读取文件
    try:
        reader = FileReader()
        content = reader.read_file(file_path)
        print(f"✅ 文件读取成功，共 {len(content)} 字符\n")
    except Exception as e:
        print(f"❌ 读取失败: {e}")
        return

    # 初始化问答
    print("⏳ 正在初始化问答系统...")
    qa_agent = QAAgent()
    qa_agent.set_context(content)
    print("✅ 问答系统已就绪！\n")

    print("💡 提示：输入 'quit' 或 'exit' 退出")
    print("-" * 60 + "\n")

    # 问答循环
    while True:
        question = input("你的问题: ").strip()

        if question.lower() in ['quit', 'exit', 'q']:
            print("\n👋 再见！")
            break

        if not question:
            continue

        print("\n⏳ 思考中...")
        try:
            answer = qa_agent.ask(question)
            print("\n💡 回答:")
            print(answer)
            print("\n" + "-" * 60 + "\n")
        except Exception as e:
            print(f"\n❌ 出错了: {e}\n")

if __name__ == "__main__":
    main()

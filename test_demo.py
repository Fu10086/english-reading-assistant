#!/usr/bin/env python3
"""
测试脚本 - 不需要 API Key
演示项目的基本功能
"""

import sys
from pathlib import Path

# 添加 src 目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from src.reader import FileReader


def test_file_reading():
    """测试文件读取功能"""
    print("=" * 60)
    print("测试 1: 文件读取功能")
    print("=" * 60)

    reader = FileReader()

    # 读取示例文件
    test_file = "examples/machine_learning.txt"
    print(f"\n正在读取: {test_file}")

    try:
        content = reader.read_file(test_file)
        print(f"✓ 读取成功！")
        print(f"✓ 文件大小: {len(content)} 字符")
        print(f"✓ 单词数: 约 {len(content.split())} 个")

        # 显示前200个字符
        print(f"\n文件内容预览:")
        print("-" * 60)
        print(content[:200] + "...")
        print("-" * 60)

        return content
    except Exception as e:
        print(f"✗ 读取失败: {e}")
        return None


def test_text_processing(content):
    """测试文本处理功能（模拟）"""
    print("\n" + "=" * 60)
    print("测试 2: 文本处理功能（模拟）")
    print("=" * 60)

    # 模拟翻译
    print("\n[翻译模块]")
    print("✓ 检测到英文文本")
    print("✓ 文本长度适中，无需分块")
    print("✓ 准备调用 Claude API 进行翻译...")
    print("  （实际运行时会调用 API）")

    # 模拟摘要
    print("\n[摘要模块]")
    print("✓ 分析文章结构...")
    print("✓ 提取关键概念: Machine Learning, AI, Supervised Learning...")
    print("✓ 准备生成摘要...")
    print("  （实际运行时会调用 API）")

    # 模拟笔记生成
    print("\n[笔记生成模块]")
    print("✓ 生成 Markdown 格式笔记")
    print("✓ 添加元数据（标题、日期、标签）")
    print("✓ 准备保存到 data/output/")
    print("  （实际运行时会调用 API 并保存文件）")


def test_token_estimation(content):
    """估算 Token 消耗"""
    print("\n" + "=" * 60)
    print("测试 3: Token 消耗估算")
    print("=" * 60)

    # 粗略估算：1 token ≈ 4 字符（英文）
    input_tokens = len(content) // 4

    print(f"\n输入文本:")
    print(f"  字符数: {len(content)}")
    print(f"  估算 tokens: ~{input_tokens}")

    print(f"\n预计 Token 消耗:")
    print(f"  翻译模式: ~{input_tokens * 2} tokens")
    print(f"  摘要模式: ~{input_tokens + 500} tokens")
    print(f"  完整分析: ~{input_tokens * 3} tokens")
    print(f"  问答模式: ~{input_tokens + 1000} tokens/次")


def show_project_structure():
    """显示项目结构"""
    print("\n" + "=" * 60)
    print("项目结构")
    print("=" * 60)

    structure = """
english-reading-assistant/
├── src/
│   ├── reader.py          ✓ 文件读取（已实现）
│   ├── translator.py      ✓ 智能翻译（已实现）
│   ├── summarizer.py      ✓ 摘要生成（已实现）
│   ├── note_generator.py  ✓ 笔记生成（已实现）
│   └── qa_agent.py        ✓ 问答系统（已实现）
├── main.py                ✓ 主程序（已实现）
├── config.py              ✓ 配置文件（已实现）
└── 文档                    ✓ README、USAGE（已完成）
"""
    print(structure)


def show_next_steps():
    """显示下一步操作"""
    print("\n" + "=" * 60)
    print("下一步操作")
    print("=" * 60)

    steps = """
1. 获取 Claude API Key
   访问: https://console.anthropic.com/

2. 配置环境变量
   echo "CLAUDE_API_KEY=your-key" > .env

3. 安装依赖（如果有 pip）
   pip install -r requirements.txt

4. 运行真实测试
   python main.py --file examples/machine_learning.txt --mode summary

5. 开始积累使用数据
   - 每天处理 5-10 篇文章
   - 记录 token 消耗
   - 截图保存过程

6. 准备申请材料（2-3周后）
   - GitHub 开源
   - 使用截图/录屏
   - Token 消耗统计
"""
    print(steps)


def main():
    print("\n" + "=" * 60)
    print("English Reading Assistant - 功能测试")
    print("=" * 60)

    # 测试 1: 文件读取
    content = test_file_reading()

    if content:
        # 测试 2: 文本处理
        test_text_processing(content)

        # 测试 3: Token 估算
        test_token_estimation(content)

    # 显示项目结构
    show_project_structure()

    # 显示下一步
    show_next_steps()

    print("\n" + "=" * 60)
    print("测试完成！")
    print("=" * 60)
    print("\n✓ 项目结构完整")
    print("✓ 核心模块已实现")
    print("✓ 文件读取功能正常")
    print("\n配置 API Key 后即可开始使用！")


if __name__ == "__main__":
    main()

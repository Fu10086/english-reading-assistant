import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# Claude API 配置
CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY", "")
MODEL = "claude-sonnet-4-6"

# 输出配置
OUTPUT_DIR = "data/output"
INPUT_DIR = "data/input"

# 翻译配置
TRANSLATION_PROMPT = """你是一个专业的技术文档翻译助手。请将以下英文内容翻译成中文，要求：
1. 保留专业术语的英文原文（在括号中标注）
2. 保持原文的段落结构
3. 翻译要准确、流畅、符合中文表达习惯
4. 对于代码、公式等技术内容，保持原样

英文原文：
{text}

请提供翻译："""

# 摘要配置
SUMMARY_PROMPT = """请为以下英文文章生成一个结构化的摘要，包括：
1. 核心观点（3-5个要点）
2. 关键概念和术语
3. 文章结构概述
4. 重要结论

文章内容：
{text}

请生成摘要："""

# 笔记生成配置
NOTE_PROMPT = """请为以下英文文章生成一份学习笔记，格式为 Markdown，包括：
1. 标题和概述
2. 核心知识点（分点列出）
3. 重要概念解释
4. 示例和代码（如果有）
5. 总结和思考

文章内容：
{text}

请生成笔记："""

# 问答配置
QA_PROMPT = """基于以下文章内容，回答用户的问题。要求：
1. 答案要准确，基于文章内容
2. 如果文章中没有相关信息，明确说明
3. 可以适当扩展和解释

文章内容：
{text}

用户问题：{question}

请回答："""

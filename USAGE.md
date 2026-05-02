# 使用指南

## 快速开始

### 1. 安装依赖

```bash
cd /home/ubuntu/english-reading-assistant
pip install -r requirements.txt
```

### 2. 配置 API Key

创建 `.env` 文件：

```bash
cp .env.example .env
# 然后编辑 .env 文件，填入你的 Claude API Key
```

或者直接设置环境变量：

```bash
export CLAUDE_API_KEY="your-api-key-here"
```

### 3. 准备测试文件

将英文文章放到 `data/input/` 目录下，支持格式：
- `.txt` - 纯文本
- `.md` - Markdown
- `.pdf` - PDF 文档

### 4. 运行示例

```bash
# 完整分析（翻译+摘要+笔记）
python main.py --file data/input/article.txt --mode full

# 只翻译
python main.py --file data/input/article.txt --mode translate

# 只生成摘要
python main.py --file data/input/article.txt --mode summary

# 生成学习笔记
python main.py --file data/input/article.txt --mode note

# 交互式问答
python main.py --file data/input/article.txt --interactive
```

## 功能说明

### 翻译模式 (translate)
- 智能翻译，保留专业术语
- 自动处理长文本（分块翻译）
- 保持原文段落结构

### 摘要模式 (summary)
- 提取核心观点
- 识别关键概念
- 生成结构化摘要

### 笔记模式 (note)
- 生成 Markdown 格式笔记
- 包含元数据（标题、日期、标签）
- 自动保存到 `data/output/` 目录

### 完整模式 (full)
- 翻译 + 摘要 + 笔记
- 一次性完成所有分析
- 生成完整的学习资料

### 问答模式 (qa)
- 基于文章内容的智能问答
- 支持多轮对话
- 交互式学习

## 使用技巧

1. **处理长文档**：程序会自动分块处理，无需担心长度限制

2. **保存输出**：所有生成的笔记自动保存在 `data/output/` 目录

3. **批量处理**：可以写脚本批量处理多个文件

4. **自定义提示词**：修改 `config.py` 中的提示词模板

## 常见问题

**Q: API Key 在哪里获取？**
A: 访问 https://console.anthropic.com/ 注册并获取

**Q: 支持哪些文件格式？**
A: 目前支持 .txt, .md, .pdf

**Q: 如何处理 PDF 文件？**
A: 直接使用 `--file your.pdf` 即可，程序会自动提取文本

**Q: 翻译质量如何？**
A: 使用 Claude Sonnet 4.6，专门针对技术文档优化

## 下一步

- 尝试用你的 CSAPP 教材或论文测试
- 根据需要调整 `config.py` 中的提示词
- 开发更多功能（生词本、知识图谱等）

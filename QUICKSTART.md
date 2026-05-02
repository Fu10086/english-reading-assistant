# 英文阅读助手 - 快速使用指南

## 🚀 快速开始

### 1. 激活虚拟环境
```bash
cd /home/ubuntu/english-reading-assistant
source venv/bin/activate
```

### 2. 基本使用

#### 📝 生成摘要（最快）
```bash
python main.py --file examples/machine_learning.txt --mode summary
```
**用途**：快速了解文章核心内容，5分钟掌握全文

#### 🌐 翻译文章
```bash
python main.py --file examples/machine_learning.txt --mode translate
```
**用途**：将英文翻译成中文，保留专业术语

#### 📚 生成学习笔记
```bash
python main.py --file examples/machine_learning.txt --mode note
```
**用途**：自动生成 Markdown 格式笔记，保存到 data/output/

#### 🎯 完整分析（推荐）
```bash
python main.py --file examples/machine_learning.txt --mode full
```
**用途**：翻译 + 摘要 + 笔记，一次性完成所有处理

#### ❓ 交互式问答
```bash
python main.py --file examples/machine_learning.txt --interactive
```
**用途**：针对文章内容提问，多轮对话学习

---

## 📂 处理你自己的文章

### 方法1：复制文件
```bash
# 复制你的英文文章到 input 目录
cp 你的文章.txt data/input/

# 处理
python main.py --file data/input/你的文章.txt --mode full
```

### 方法2：直接创建文件
```bash
# 创建新文件
nano data/input/my_article.txt

# 粘贴英文内容，保存（Ctrl+O, Enter, Ctrl+X）

# 处理
python main.py --file data/input/my_article.txt --mode summary
```

### 方法3：从网上下载
```bash
# 下载英文文章
wget https://example.com/article.txt -O data/input/article.txt

# 处理
python main.py --file data/input/article.txt --mode full
```

---

## 💡 实际使用场景

### 场景1：学习 CSAPP 教材
```bash
# 1. 复制教材章节
cp ~/CSAPP_Chapter3.txt data/input/

# 2. 完整分析
python main.py --file data/input/CSAPP_Chapter3.txt --mode full

# 3. 查看生成的笔记
ls data/output/
cat data/output/note_*.md
```

### 场景2：快速了解论文
```bash
# 1. 先生成摘要，快速判断是否值得深入阅读
python main.py --file paper.txt --mode summary

# 2. 如果感兴趣，再做完整分析
python main.py --file paper.txt --mode full
```

### 场景3：学习技术博客
```bash
# 1. 翻译
python main.py --file blog.txt --mode translate

# 2. 如果有疑问，进入问答模式
python main.py --file blog.txt --interactive
```

---

## 📊 查看使用统计

```bash
python usage_tracker.py
```

显示：
- 处理了多少篇文章
- 消耗了多少 token
- 日均/月均使用量

---

## 🎯 每天的使用流程

### 早上（10分钟）
```bash
# 1. 找 2-3 篇英文资料
# 2. 生成摘要，快速筛选
python main.py --file article1.txt --mode summary
python main.py --file article2.txt --mode summary

# 3. 选择感兴趣的深入学习
python main.py --file article1.txt --mode full
```

### 晚上（20分钟）
```bash
# 1. 复习生成的笔记
ls data/output/
cat data/output/note_20260502_*.md

# 2. 如果有疑问，进入问答模式
python main.py --file article1.txt --interactive
```

---

## 🔧 常见问题

### Q1: 如何处理 PDF 文件？
A: 需要先转成 txt 格式：
```bash
# 方法1：使用 pdftotext（需要安装）
pdftotext paper.pdf paper.txt

# 方法2：复制 PDF 内容到文本文件
nano paper.txt  # 粘贴内容
```

### Q2: 文章太长怎么办？
A: 系统会自动分块处理，支持 10000+ 词的长文档

### Q3: 如何批量处理多篇文章？
A: 使用循环：
```bash
for file in data/input/*.txt; do
    echo "处理: $file"
    python main.py --file "$file" --mode summary
done
```

### Q4: 生成的笔记在哪里？
A: 在 `data/output/` 目录，文件名格式：`note_20260502_143000.md`

### Q5: 如何查看 API 消耗？
A: 运行 `python usage_tracker.py`

---

## 📝 使用技巧

### 技巧1：先摘要后全文
```bash
# 先快速浏览摘要（省 token）
python main.py --file article.txt --mode summary

# 如果感兴趣，再做完整分析
python main.py --file article.txt --mode full
```

### 技巧2：保存重要笔记
```bash
# 生成笔记后，复制到你的笔记系统
cp data/output/note_*.md ~/Obsidian/学习笔记/
```

### 技巧3：问答模式深度学习
```bash
# 进入交互模式
python main.py --file article.txt --interactive

# 可以问的问题：
# - 什么是 XXX？
# - XXX 和 YYY 的区别？
# - 能举个例子吗？
# - 这个概念在实际中如何应用？
```

---

## 🎓 学习建议

### 第1周：熟悉工具
- 每天处理 2-3 篇短文章（1000 词左右）
- 尝试所有模式（翻译、摘要、笔记、问答）
- 找到最适合你的使用方式

### 第2-4周：积累数据
- 每天处理 5-10 篇文章
- 重点处理你的课程相关资料
- 记录使用数据和效果

### 长期使用
- 建立自己的知识库
- 定期复习生成的笔记
- 用问答模式巩固理解

---

## 📞 需要帮助？

- 查看详细文档：`cat USAGE.md`
- 查看项目介绍：`cat README.md`
- GitHub 仓库：https://github.com/Fu10086/english-reading-assistant

---

**现在就开始使用吧！** 🚀

# 📖 使用指南

## 🚀 三种使用方式

### 方式1：命令行工具

```bash
# 激活环境
cd /home/ubuntu/english-reading-assistant
source venv/bin/activate

# 基本用法
python main.py --file <文件路径> --mode <模式>
```

**处理模式：**
- `summary` - 生成摘要（最快，5分钟）
- `translate` - 智能翻译
- `note` - 生成学习笔记
- `full` - 完整分析（翻译+摘要+笔记）
- `--interactive` - 交互式问答

**示例：**
```bash
# 快速摘要
python main.py --file article.pdf --mode summary

# 完整分析
python main.py --file paper.pdf --mode full

# 问答模式
python main.py --file document.txt --interactive
```

---

### 方式2：交互式菜单（推荐新手）

```bash
python interactive.py
```

**特点：**
- ✅ 菜单式操作，简单直观
- ✅ 支持所有功能
- ✅ 不需要记命令

**使用流程：**
1. 选择功能（1-5）
2. 输入文件路径或粘贴文本
3. 等待处理完成
4. 查看结果

---

### 方式3：Web 图形界面

```bash
# 启动服务
streamlit run app.py --server.port 7860 --server.address 0.0.0.0

# 访问（需要 SSH 端口转发）
# 在本地电脑运行：
ssh -L 7860:localhost:7860 ubuntu@服务器IP

# 浏览器访问：
http://localhost:7860
```

**特点：**
- ✅ 图形化界面，更美观
- ✅ 支持文件上传
- ✅ 实时显示进度
- ✅ 支持下载结果

---

## 📂 文件格式支持

### TXT / MD 文件
```bash
python main.py --file article.txt --mode summary
```

### PDF 文件
```bash
# 自动解析 PDF
python main.py --file paper.pdf --mode full

# 显示 PDF 信息
python -c "from src.pdf_reader import PDFReader; r = PDFReader(); print(r.get_pdf_info('paper.pdf'))"
```

---

## 🎯 实际使用场景

### 场景1：学习 CSAPP 教材

```bash
# 1. 复制教材章节
cp ~/CSAPP_Chapter3.pdf data/input/

# 2. 完整分析
python main.py --file data/input/CSAPP_Chapter3.pdf --mode full

# 3. 查看生成的笔记
ls data/output/
cat data/output/note_*.md
```

### 场景2：快速了解论文

```bash
# 1. 先生成摘要（省 token）
python main.py --file paper.pdf --mode summary

# 2. 如果感兴趣，再做完整分析
python main.py --file paper.pdf --mode full

# 3. 如有疑问，进入问答模式
python main.py --file paper.pdf --interactive
```

### 场景3：批量处理多篇文章

```bash
# 处理整个目录
python batch_process.py data/input summary

# 完整分析整个目录
python batch_process.py data/input full

# 查看处理报告
cat data/output/batch/report_*.json
```

---

## 💡 使用技巧

### 技巧1：先摘要后全文（节省 token）

```bash
# 1. 快速浏览摘要
python main.py --file article.pdf --mode summary

# 2. 如果感兴趣，再做完整分析
python main.py --file article.pdf --mode full
```

### 技巧2：批量处理提高效率

```bash
# 一次处理多个文件
python batch_process.py data/input summary

# 自动生成处理报告
```

### 技巧3：问答模式深度学习

```bash
python main.py --file article.pdf --interactive

# 可以问的问题：
# - 这篇文章的核心观点是什么？
# - XXX 和 YYY 有什么区别？
# - 能举个例子说明 XXX 吗？
# - 这个概念在实际中如何应用？
```

### 技巧4：保存重要笔记

```bash
# 生成的笔记在 data/output/
ls data/output/

# 复制到你的笔记系统
cp data/output/note_*.md ~/Obsidian/学习笔记/
```

---

## 📊 使用统计

### 查看统计报告

```bash
python usage_analyzer.py
```

**输出示例：**
```
📊 使用统计报告（最近 30 天）
============================================================
📈 总体统计
  处理文章: 50 篇
  处理字符: 150,000 字符
  消耗 Token: 1,500,000
  平均每篇: 30,000 tokens

📊 按模式统计
  summary: 20 篇, 300,000 tokens
  full: 15 篇, 900,000 tokens
  translate: 15 篇, 300,000 tokens

🔮 预测
  日均消耗: 50,000 tokens
  月预测: 1,500,000 tokens
```

### 导出数据

```bash
# 导出 CSV
python usage_analyzer.py export

# 查看导出文件
cat data/usage_report.csv
```

---

## 🔧 常见问题

### Q1: 如何处理 PDF 文件？
**A:** 直接使用，自动解析：
```bash
python main.py --file document.pdf --mode summary
```

### Q2: 文章太长怎么办？
**A:** 系统自动分块处理，支持 10000+ 词的长文档。

### Q3: 如何批量处理？
**A:** 使用批量处理工具：
```bash
python batch_process.py data/input summary
```

### Q4: 生成的笔记在哪里？
**A:** 在 `data/output/` 目录，文件名格式：`note_20260502_143000.md`

### Q5: 如何查看 API 消耗？
**A:** 运行 `python usage_analyzer.py`

### Q6: Web 界面无法访问？
**A:** 使用 SSH 端口转发：
```bash
# 在本地电脑运行
ssh -L 7860:localhost:7860 ubuntu@服务器IP

# 然后访问 http://localhost:7860
```

---

## 🎓 学习建议

### 第1周：熟悉工具
- 每天处理 2-3 篇短文章（1000 词左右）
- 尝试所有模式
- 找到最适合你的使用方式

### 第2-4周：积累数据
- 每天处理 5-10 篇文章
- 重点处理课程相关资料
- 记录使用数据和效果

### 长期使用
- 建立自己的知识库
- 定期复习生成的笔记
- 用问答模式巩固理解

---

## 📞 获取帮助

- **GitHub Issues**: https://github.com/Fu10086/english-reading-assistant/issues
- **查看 README**: `cat README.md`
- **查看申请材料**: `cat APPLICATION_FINAL.md`

---

**祝学习愉快！** 🎉

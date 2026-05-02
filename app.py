"""
英文阅读助手 - 现代化 Web 界面
参考 ChatGPT、Claude、Notion AI 的设计
"""

import streamlit as st
import os
from pathlib import Path
from datetime import datetime

# 导入核心模块
from src.translator import Translator
from src.summarizer import Summarizer
from src.note_generator import NoteGenerator
from src.qa_agent import QAAgent
from src.reader import FileReader

# 页面配置
st.set_page_config(
    page_title="英文阅读助手 | AI Reading Assistant",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 现代化 CSS 样式
st.markdown("""
<style>
    /* 全局样式 */
    .main {
        background-color: #ffffff;
    }

    /* 隐藏 Streamlit 默认元素 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* 主标题 */
    .main-title {
        font-size: 2.8rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
        padding: 1rem 0;
    }

    .subtitle {
        text-align: center;
        color: #6b7280;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }

    /* 卡片样式 */
    .card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
        border: 1px solid #e5e7eb;
    }

    /* 结果容器 - 类似 ChatGPT */
    .result-container {
        background: #f9fafb;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid #e5e7eb;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        line-height: 1.7;
        color: #1f2937;
    }

    .result-container h1,
    .result-container h2,
    .result-container h3 {
        color: #111827;
        margin-top: 1.5rem;
        margin-bottom: 0.75rem;
        font-weight: 600;
    }

    .result-container h1 { font-size: 1.875rem; }
    .result-container h2 { font-size: 1.5rem; }
    .result-container h3 { font-size: 1.25rem; }

    .result-container p {
        margin-bottom: 1rem;
        line-height: 1.7;
    }

    .result-container ul,
    .result-container ol {
        margin-left: 1.5rem;
        margin-bottom: 1rem;
    }

    .result-container li {
        margin-bottom: 0.5rem;
    }

    .result-container code {
        background: #f3f4f6;
        padding: 0.2rem 0.4rem;
        border-radius: 4px;
        font-family: 'Monaco', 'Courier New', monospace;
        font-size: 0.9em;
        color: #dc2626;
    }

    .result-container pre {
        background: #1f2937;
        color: #f9fafb;
        padding: 1rem;
        border-radius: 8px;
        overflow-x: auto;
    }

    /* 问答气泡 - 类似 ChatGPT */
    .question-bubble {
        background: #f3f4f6;
        border-radius: 12px;
        padding: 1rem 1.25rem;
        margin: 1rem 0;
        border-left: 4px solid #667eea;
    }

    .answer-bubble {
        background: #ffffff;
        border-radius: 12px;
        padding: 1.25rem;
        margin: 1rem 0;
        border: 1px solid #e5e7eb;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
    }

    /* 统计卡片 */
    .stat-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 12px;
        padding: 1.25rem;
        text-align: center;
        box-shadow: 0 4px 6px rgba(102, 126, 234, 0.3);
    }

    .stat-number {
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 0.25rem;
    }

    .stat-label {
        font-size: 0.875rem;
        opacity: 0.9;
    }

    /* 按钮优化 */
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(102, 126, 234, 0.3);
    }

    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(102, 126, 234, 0.4);
    }

    /* 下载按钮 */
    .stDownloadButton>button {
        background: white;
        color: #667eea;
        border: 2px solid #667eea;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }

    .stDownloadButton>button:hover {
        background: #667eea;
        color: white;
    }

    /* 标签页优化 */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: #f9fafb;
        padding: 0.5rem;
        border-radius: 12px;
    }

    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        color: #6b7280;
    }

    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background: white;
        color: #667eea;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }

    /* 输入框优化 */
    .stTextInput>div>div>input,
    .stTextArea>div>div>textarea {
        border-radius: 8px;
        border: 2px solid #e5e7eb;
        padding: 0.75rem;
        font-size: 1rem;
    }

    .stTextInput>div>div>input:focus,
    .stTextArea>div>div>textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }

    /* 文件上传器优化 - 大面积拖拽区域 */
    .stFileUploader {
        border: 3px dashed #e5e7eb;
        border-radius: 16px;
        padding: 3rem 2rem;
        text-align: center;
        transition: all 0.3s ease;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%);
        cursor: pointer;
        position: relative;
    }

    .stFileUploader:hover {
        border-color: #667eea;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
        transform: scale(1.02);
        box-shadow: 0 8px 16px rgba(102, 126, 234, 0.2);
    }

    /* 拖拽提示文字 */
    .stFileUploader section {
        padding: 2rem;
    }

    .stFileUploader section > div {
        font-size: 1.1rem;
        color: #667eea;
        font-weight: 600;
    }

    /* 拖拽时的动画效果 */
    .stFileUploader[data-drag-active="true"] {
        border-color: #667eea;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.15) 0%, rgba(118, 75, 162, 0.15) 100%);
        transform: scale(1.05);
        box-shadow: 0 12px 24px rgba(102, 126, 234, 0.3);
    }

    /* 成功/错误/信息提示优化 */
    .stSuccess, .stError, .stInfo, .stWarning {
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }

    /* 侧边栏优化 */
    .css-1d391kg {
        background: #f9fafb;
    }

    /* Metric 优化 */
    [data-testid="stMetricValue"] {
        font-size: 1.75rem;
        font-weight: 700;
        color: #667eea;
    }

    /* 滚动条优化 */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }

    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
    }

    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #5568d3 0%, #6a3f8f 100%);
    }

    /* 加载动画 */
    .stSpinner > div {
        border-top-color: #667eea !important;
    }
</style>
""", unsafe_allow_html=True)

# 初始化 session state
if 'processed_text' not in st.session_state:
    st.session_state.processed_text = None
if 'current_file_content' not in st.session_state:
    st.session_state.current_file_content = None
if 'qa_agent' not in st.session_state:
    st.session_state.qa_agent = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# 主标题
st.markdown('<div class="main-title">📚 英文阅读助手</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">AI-Powered English Reading Assistant | 让英文阅读更简单</div>', unsafe_allow_html=True)

# 侧边栏
with st.sidebar:
    st.markdown("### ⚙️ 系统设置")

    # API 状态卡片
    try:
        import config
        api_type = config.API_TYPE
        model = config.MODEL

        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-label">API 状态</div>
            <div class="stat-number">✓</div>
            <div class="stat-label">{api_type.upper()} · {model}</div>
        </div>
        """, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"❌ API 配置错误")

    st.markdown("---")

    # 使用统计
    st.markdown("### 📊 使用统计")
    output_dir = Path("data/output")
    if output_dir.exists():
        note_count = len(list(output_dir.glob("*.md")))
    else:
        note_count = 0

    col1, col2 = st.columns(2)
    with col1:
        st.metric("📝 笔记", note_count)
    with col2:
        st.metric("🎯 模式", "5种")

    st.markdown("---")

    # 快速指南
    st.markdown("### 💡 快速指南")
    with st.expander("📖 如何使用", expanded=False):
        st.markdown("""
        **1. 输入内容**
        - 上传文件 (TXT/MD/PDF)
        - 或直接粘贴文本

        **2. 选择模式**
        - 摘要：快速了解
        - 翻译：准确翻译
        - 笔记：系统整理
        - 完整：一次搞定
        - 问答：深度理解

        **3. 开始处理**
        - 点击按钮即可
        - 结果可直接复制
        """)

    st.markdown("---")
    st.markdown("🔗 [GitHub](https://github.com/Fu10086/english-reading-assistant)")
    st.caption("Made with ❤️ by Claude Sonnet 4.6")

# 主界面 - 两栏布局
col_left, col_right = st.columns([1, 1], gap="large")

with col_left:
    st.markdown("### 📥 输入内容")

    # 输入方式选择
    input_tab1, input_tab2 = st.tabs(["📁 上传文件", "✍️ 粘贴文本"])

    content = None

    with input_tab1:
        # 添加拖拽提示
        st.markdown("""
        <div style='text-align: center; padding: 1rem 0; color: #667eea;'>
            <h3 style='margin: 0; font-size: 1.5rem;'>📁 拖拽文件到这里</h3>
            <p style='margin: 0.5rem 0; color: #6b7280;'>或点击选择文件</p>
            <p style='margin: 0; font-size: 0.9rem; color: #9ca3af;'>支持 TXT、MD、PDF 格式</p>
        </div>
        """, unsafe_allow_html=True)

        uploaded_file = st.file_uploader(
            "选择文件",
            type=['txt', 'md', 'pdf'],
            help="拖拽文件到上方区域，或点击选择文件",
            label_visibility="collapsed"
        )

        if uploaded_file is not None:
            # 根据文件类型处理
            if uploaded_file.name.endswith('.pdf'):
                import tempfile
                from src.pdf_reader import PDFReader

                with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                    tmp_file.write(uploaded_file.read())
                    tmp_path = tmp_file.name

                try:
                    pdf_reader = PDFReader()
                    info = pdf_reader.get_pdf_info(tmp_path)

                    st.success(f"✅ {uploaded_file.name}")

                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.metric("📄 页数", info.get('pages', 'N/A'))
                    with col_b:
                        st.metric("📝 字符", info.get('estimated_chars', 'N/A'))

                    with st.spinner("⏳ 解析 PDF..."):
                        content = pdf_reader.read_pdf(tmp_path)

                    st.success("✅ 解析完成")

                except Exception as e:
                    st.error(f"❌ 解析失败: {e}")
                    content = None
                finally:
                    if os.path.exists(tmp_path):
                        os.unlink(tmp_path)
            else:
                content = uploaded_file.read().decode('utf-8')
                st.success(f"✅ {uploaded_file.name}")
                st.metric("📝 字符数", len(content))

            # 预览
            if content:
                with st.expander("👀 预览内容", expanded=False):
                    preview = content[:800] + "..." if len(content) > 800 else content
                    st.text(preview)

    with input_tab2:
        content = st.text_area(
            "粘贴英文文本",
            height=300,
            placeholder="在这里粘贴你的英文文章...\n\n支持长文本，系统会自动分块处理",
            label_visibility="collapsed"
        )

        if content:
            st.metric("📝 字符数", len(content))

    # 处理模式选择
    st.markdown("### 🎯 处理模式")

    mode_options = {
        "⚡ 摘要 (最快)": "快速生成核心摘要，5分钟掌握全文",
        "🌐 翻译": "智能翻译，保留专业术语",
        "📝 笔记生成": "生成 Markdown 学习笔记",
        "🎯 完整分析": "翻译 + 摘要 + 笔记，一次性完成",
        "💬 问答模式": "交互式问答，深度理解"
    }

    mode = st.selectbox(
        "选择模式",
        list(mode_options.keys()),
        label_visibility="collapsed"
    )

    st.info(mode_options[mode])

    # 开始处理按钮
    process_button = st.button("🚀 开始处理", type="primary", use_container_width=True)

with col_right:
    st.markdown("### 📤 处理结果")

    if process_button and content:
        st.session_state.current_file_content = content

        with st.spinner("⏳ AI 正在处理中..."):
            try:
                # 摘要模式
                if "摘要" in mode:
                    summarizer = Summarizer()
                    result = summarizer.summarize(content)
                    st.session_state.processed_text = result

                    st.success("✅ 摘要生成完成！")

                    st.metric("📊 摘要字数", f"{len(result)} 字")

                    st.markdown('<div class="result-container">', unsafe_allow_html=True)
                    st.markdown(result)
                    st.markdown('</div>', unsafe_allow_html=True)

                    st.download_button(
                        label="📥 下载摘要",
                        data=result,
                        file_name=f"summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                        mime="text/markdown",
                        use_container_width=True
                    )

                # 翻译模式
                elif "翻译" in mode:
                    translator = Translator()
                    result = translator.translate(content)
                    st.session_state.processed_text = result

                    st.success("✅ 翻译完成！")

                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.metric("📊 翻译字数", f"{len(result)} 字")
                    with col_b:
                        st.metric("📄 原文字符", f"{len(content)} 字符")

                    st.markdown('<div class="result-container">', unsafe_allow_html=True)
                    st.markdown(result)
                    st.markdown('</div>', unsafe_allow_html=True)

                    st.download_button(
                        label="📥 下载翻译",
                        data=result,
                        file_name=f"translation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                        mime="text/markdown",
                        use_container_width=True
                    )

                # 笔记生成模式
                elif "笔记" in mode:
                    note_gen = NoteGenerator()
                    result = note_gen.generate_note(content)
                    st.session_state.processed_text = result

                    saved_path = note_gen.save_note(result)

                    st.success("✅ 笔记生成完成！")
                    st.info(f"💾 已保存: {saved_path}")

                    st.metric("📊 笔记字数", f"{len(result)} 字")

                    st.markdown('<div class="result-container">', unsafe_allow_html=True)
                    st.markdown(result)
                    st.markdown('</div>', unsafe_allow_html=True)

                    st.download_button(
                        label="📥 下载笔记",
                        data=result,
                        file_name=f"note_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                        mime="text/markdown",
                        use_container_width=True
                    )

                # 完整分析模式
                elif "完整" in mode:
                    with st.status("🔄 正在处理...", expanded=True) as status:
                        st.write("⏳ 翻译中...")
                        translator = Translator()
                        translation = translator.translate(content)
                        st.write("✅ 翻译完成")

                        st.write("⏳ 生成摘要...")
                        summarizer = Summarizer()
                        summary = summarizer.summarize(content)
                        st.write("✅ 摘要完成")

                        st.write("⏳ 生成笔记...")
                        note_gen = NoteGenerator()
                        note = note_gen.generate_note(content)
                        saved_path = note_gen.save_note(note)
                        st.write("✅ 笔记完成")

                        status.update(label="✅ 完整分析完成！", state="complete")

                    # 标签页显示结果
                    tab1, tab2, tab3 = st.tabs(["📋 摘要", "🌐 翻译", "📝 笔记"])

                    with tab1:
                        st.metric("📊 字数", f"{len(summary)} 字")
                        st.markdown('<div class="result-container">', unsafe_allow_html=True)
                        st.markdown(summary)
                        st.markdown('</div>', unsafe_allow_html=True)
                        st.download_button(
                            "📥 下载",
                            summary,
                            f"summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                            use_container_width=True
                        )

                    with tab2:
                        st.metric("📊 字数", f"{len(translation)} 字")
                        st.markdown('<div class="result-container">', unsafe_allow_html=True)
                        st.markdown(translation)
                        st.markdown('</div>', unsafe_allow_html=True)
                        st.download_button(
                            "📥 下载",
                            translation,
                            f"translation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                            use_container_width=True
                        )

                    with tab3:
                        st.metric("📊 字数", f"{len(note)} 字")
                        st.markdown('<div class="result-container">', unsafe_allow_html=True)
                        st.markdown(note)
                        st.markdown('</div>', unsafe_allow_html=True)
                        st.download_button(
                            "📥 下载",
                            note,
                            f"note_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                            use_container_width=True
                        )

                # 问答模式
                elif "问答" in mode:
                    if st.session_state.qa_agent is None or st.session_state.current_file_content != content:
                        st.session_state.qa_agent = QAAgent()
                        st.session_state.qa_agent.set_context(content)
                        st.session_state.current_file_content = content
                        st.session_state.chat_history = []

                    st.success("✅ 问答模式已激活！")

                    # 提问区
                    question = st.text_input(
                        "💬 输入你的问题",
                        placeholder="例如：这篇文章的核心观点是什么？",
                        label_visibility="collapsed"
                    )

                    ask_button = st.button("🚀 提问", type="primary", use_container_width=True)

                    if ask_button and question:
                        with st.spinner("⏳ AI 正在思考..."):
                            try:
                                answer = st.session_state.qa_agent.ask(question)
                                st.session_state.chat_history.append((question, answer))
                            except Exception as e:
                                st.error(f"❌ 回答失败: {e}")

                    # 显示对话历史
                    if st.session_state.chat_history:
                        st.markdown("---")
                        st.markdown("### 💬 对话历史")

                        for i, (q, a) in enumerate(reversed(st.session_state.chat_history)):
                            question_num = len(st.session_state.chat_history) - i

                            # 问题气泡
                            st.markdown(f"""
                            <div class="question-bubble">
                                <strong>💬 问题 {question_num}:</strong> {q}
                            </div>
                            """, unsafe_allow_html=True)

                            # 回答气泡
                            st.markdown('<div class="answer-bubble">', unsafe_allow_html=True)
                            st.markdown(a)
                            st.markdown('</div>', unsafe_allow_html=True)

            except Exception as e:
                st.error(f"❌ 处理失败: {str(e)}")
                with st.expander("🔍 错误详情"):
                    st.exception(e)

    elif process_button and not content:
        st.warning("⚠️ 请先输入内容")

    else:
        # 默认显示
        st.info("👈 请在左侧输入内容并选择处理模式")

        # 功能介绍
        with st.expander("✨ 功能特点", expanded=True):
            st.markdown("""
            **🎯 五种处理模式**
            - ⚡ 摘要：快速提取核心要点
            - 🌐 翻译：保留术语的智能翻译
            - 📝 笔记：结构化学习笔记
            - 🎯 完整：一次性全部完成
            - 💬 问答：交互式深度理解

            **💡 智能特性**
            - 自动分块处理长文本
            - 保留专业术语原文
            - 生成 Markdown 格式
            - 支持多轮对话问答

            **📊 使用建议**
            - 先用摘要快速判断价值
            - 重要内容用完整分析
            - 有疑问时用问答模式
            """)

# 页脚
st.markdown("---")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="stat-card">
        <div class="stat-number">5</div>
        <div class="stat-label">处理模式</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="stat-card">
        <div class="stat-number">3</div>
        <div class="stat-label">文件格式</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="stat-card">
        <div class="stat-number">GLM-4</div>
        <div class="stat-label">AI 模型</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="stat-card">
        <div class="stat-number">∞</div>
        <div class="stat-label">文本长度</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div style='text-align: center; padding: 2rem; color: #6b7280;'>
    <p style='font-size: 0.9rem;'>📚 英文阅读助手 | AI-Powered Reading Assistant</p>
    <p style='font-size: 0.85rem;'>
        基于智谱 GLM-4 构建 |
        <a href='https://github.com/Fu10086/english-reading-assistant' target='_blank' style='color: #667eea; text-decoration: none;'>GitHub</a> |
        Made with ❤️ by Claude Sonnet 4.6
    </p>
</div>
""", unsafe_allow_html=True)

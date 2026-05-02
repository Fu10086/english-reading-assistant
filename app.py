"""
英文阅读助手 - Streamlit Web 界面
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
    page_title="英文阅读助手",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义 CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #1f77b4;
        color: white;
        font-weight: bold;
    }
    .success-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
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

# 标题
st.markdown('<div class="main-header">📚 英文阅读助手</div>', unsafe_allow_html=True)
st.markdown("---")

# 侧边栏
with st.sidebar:
    st.header("⚙️ 设置")

    # API 状态
    st.subheader("🔌 API 状态")
    try:
        import config
        api_type = config.API_TYPE
        model = config.MODEL
        st.success(f"✅ 已连接: {api_type.upper()}")
        st.info(f"📊 模型: {model}")
    except Exception as e:
        st.error(f"❌ API 配置错误: {str(e)}")

    st.markdown("---")

    # 使用统计
    st.subheader("📊 使用统计")
    output_dir = Path("data/output")
    if output_dir.exists():
        note_count = len(list(output_dir.glob("*.md")))
        st.metric("生成笔记数", note_count)
    else:
        st.metric("生成笔记数", 0)

    st.markdown("---")

    # 帮助信息
    st.subheader("💡 使用提示")
    st.markdown("""
    1. 上传文件或粘贴文本
    2. 选择处理模式
    3. 点击开始处理
    4. 查看结果并下载
    """)

    st.markdown("---")
    st.markdown("🔗 [GitHub](https://github.com/Fu10086/english-reading-assistant)")

# 主界面
col1, col2 = st.columns([1, 1])

with col1:
    st.header("📥 输入")

    # 输入方式选择
    input_method = st.radio(
        "选择输入方式",
        ["上传文件", "粘贴文本"],
        horizontal=True
    )

    content = None

    if input_method == "上传文件":
        uploaded_file = st.file_uploader(
            "上传英文文件",
            type=['txt', 'md', 'pdf'],
            help="支持 .txt、.md 和 .pdf 格式"
        )

        if uploaded_file is not None:
            # 根据文件类型处理
            if uploaded_file.name.endswith('.pdf'):
                # PDF 文件处理
                import tempfile
                from src.pdf_reader import PDFReader

                # 保存临时文件
                with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                    tmp_file.write(uploaded_file.read())
                    tmp_path = tmp_file.name

                try:
                    # 读取 PDF
                    pdf_reader = PDFReader()

                    # 显示 PDF 信息
                    info = pdf_reader.get_pdf_info(tmp_path)
                    st.success(f"✅ PDF 已上传: {uploaded_file.name}")
                    st.info(f"📄 页数: {info.get('pages', 'N/A')} | 📝 字符数: {info.get('estimated_chars', 'N/A')}")

                    # 提取文本
                    with st.spinner("⏳ 正在解析 PDF..."):
                        content = pdf_reader.read_pdf(tmp_path)

                    st.success("✅ PDF 解析完成！")

                except Exception as e:
                    st.error(f"❌ PDF 解析失败: {e}")
                    content = None
                finally:
                    # 删除临时文件
                    import os
                    if os.path.exists(tmp_path):
                        os.unlink(tmp_path)
            else:
                # 文本文件处理
                content = uploaded_file.read().decode('utf-8')
                st.success(f"✅ 文件已上传: {uploaded_file.name}")
                st.info(f"📝 字符数: {len(content)}")

            # 预览
            with st.expander("📖 预览内容"):
                st.text_area("", content[:500] + "..." if len(content) > 500 else content, height=150, disabled=True)

    else:  # 粘贴文本
        content = st.text_area(
            "粘贴英文文本",
            height=300,
            placeholder="在这里粘贴你的英文文章..."
        )

        if content:
            st.info(f"📝 字符数: {len(content)}")

    # 处理模式选择
    st.subheader("🎯 处理模式")
    mode = st.selectbox(
        "选择处理模式",
        ["摘要 (最快)", "翻译", "笔记生成", "完整分析", "问答模式"],
        help="不同模式适用于不同场景"
    )

    # 模式说明
    mode_descriptions = {
        "摘要 (最快)": "⚡ 快速生成文章摘要，5分钟掌握核心内容",
        "翻译": "🌐 智能翻译，保留专业术语",
        "笔记生成": "📝 生成 Markdown 学习笔记",
        "完整分析": "🎯 翻译 + 摘要 + 笔记，一次性完成",
        "问答模式": "💬 交互式问答，深度理解文章"
    }
    st.info(mode_descriptions[mode])

    # 开始处理按钮
    process_button = st.button("🚀 开始处理", type="primary", use_container_width=True)

with col2:
    st.header("📤 输出")

    if process_button and content:
        st.session_state.current_file_content = content

        with st.spinner("正在处理中..."):
            try:
                if mode == "摘要 (最快)":
                    summarizer = Summarizer()
                    result = summarizer.summarize(content)
                    st.session_state.processed_text = result

                    st.success("✅ 摘要生成完成！")
                    st.markdown("### 📋 摘要结果")
                    st.markdown(result)

                    # 下载按钮
                    st.download_button(
                        label="📥 下载摘要",
                        data=result,
                        file_name=f"summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                        mime="text/markdown"
                    )

                elif mode == "翻译":
                    translator = Translator()
                    result = translator.translate(content)
                    st.session_state.processed_text = result

                    st.success("✅ 翻译完成！")
                    st.markdown("### 🌐 翻译结果")
                    st.markdown(result)

                    st.download_button(
                        label="📥 下载翻译",
                        data=result,
                        file_name=f"translation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                        mime="text/markdown"
                    )

                elif mode == "笔记生成":
                    note_gen = NoteGenerator()
                    result = note_gen.generate_note(content)
                    st.session_state.processed_text = result

                    # 保存笔记
                    saved_path = note_gen.save_note(result)

                    st.success(f"✅ 笔记生成完成！已保存到: {saved_path}")
                    st.markdown("### 📝 学习笔记")
                    st.markdown(result)

                    st.download_button(
                        label="📥 下载笔记",
                        data=result,
                        file_name=f"note_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                        mime="text/markdown"
                    )

                elif mode == "完整分析":
                    # 翻译
                    with st.status("正在翻译...", expanded=True) as status:
                        translator = Translator()
                        translation = translator.translate(content)
                        st.write("✅ 翻译完成")

                        # 摘要
                        st.write("正在生成摘要...")
                        summarizer = Summarizer()
                        summary = summarizer.summarize(content)
                        st.write("✅ 摘要完成")

                        # 笔记
                        st.write("正在生成笔记...")
                        note_gen = NoteGenerator()
                        note = note_gen.generate_note(content)
                        saved_path = note_gen.save_note(note)
                        st.write("✅ 笔记完成")

                        status.update(label="✅ 完整分析完成！", state="complete")

                    # 显示结果
                    tab1, tab2, tab3 = st.tabs(["📋 摘要", "🌐 翻译", "📝 笔记"])

                    with tab1:
                        st.markdown(summary)
                        st.download_button(
                            "📥 下载摘要",
                            summary,
                            f"summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
                        )

                    with tab2:
                        st.markdown(translation)
                        st.download_button(
                            "📥 下载翻译",
                            translation,
                            f"translation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
                        )

                    with tab3:
                        st.markdown(note)
                        st.download_button(
                            "📥 下载笔记",
                            note,
                            f"note_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
                        )

                elif mode == "问答模式":
                    # 初始化问答 Agent
                    if st.session_state.qa_agent is None or st.session_state.current_file_content != content:
                        st.session_state.qa_agent = QAAgent()
                        st.session_state.qa_agent.set_context(content)
                        st.session_state.current_file_content = content
                        st.session_state.chat_history = []  # 清空历史

                    st.success("✅ 问答模式已激活！")

                    # 使用文本输入框代替 chat_input（更明显）
                    st.markdown("### 💬 提问区")
                    question = st.text_input("输入你的问题：", key="question_input", placeholder="例如：这篇文章的核心观点是什么？")

                    ask_button = st.button("🚀 提问", type="primary", use_container_width=True)

                    if ask_button and question:
                        with st.spinner("⏳ 正在思考..."):
                            try:
                                answer = st.session_state.qa_agent.ask(question)
                                # 保存到历史
                                st.session_state.chat_history.append((question, answer))
                            except Exception as e:
                                st.error(f"❌ 回答失败: {e}")

                    # 显示聊天历史
                    if st.session_state.chat_history:
                        st.markdown("### 📝 对话历史")
                        for i, (q, a) in enumerate(st.session_state.chat_history):
                            st.markdown(f"**问题 {i+1}:** {q}")
                            st.info(a)
                            st.markdown("---")

            except Exception as e:
                st.error(f"❌ 处理失败: {str(e)}")
                st.exception(e)

    elif process_button and not content:
        st.warning("⚠️ 请先上传文件或粘贴文本")

    else:
        st.info("👈 请在左侧输入内容并选择处理模式")

# 底部信息
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("🎯 支持模式", "5种")

with col2:
    st.metric("🌐 支持格式", "TXT, MD")

with col3:
    st.metric("🤖 AI 模型", "智谱 GLM-4")

# 页脚
st.markdown("""
<div style='text-align: center; color: #666; padding: 2rem;'>
    <p>📚 英文阅读助手 | 基于智谱 AI 构建</p>
    <p>🔗 <a href='https://github.com/Fu10086/english-reading-assistant' target='_blank'>GitHub</a> |
    Made with ❤️ by Claude Sonnet 4.6</p>
</div>
""", unsafe_allow_html=True)

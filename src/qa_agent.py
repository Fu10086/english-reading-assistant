"""
问答系统模块
支持 Anthropic 和智谱 API
"""

import config


class QAAgent:
    """问答助手"""

    def __init__(self, api_key: str = None):
        """
        初始化问答助手

        Args:
            api_key: API Key
        """
        self.api_key = api_key or config.API_KEY
        if not self.api_key:
            raise ValueError("请设置 API Key 环境变量")

        # 根据 API 类型初始化客户端
        if config.USE_OPENAI_FORMAT:
            from openai import OpenAI
            self.client = OpenAI(
                api_key=self.api_key,
                base_url=config.BASE_URL
            )
        else:
            from anthropic import Anthropic
            self.client = Anthropic(
                api_key=self.api_key,
                base_url=config.BASE_URL
            )

        self.model = config.MODEL
        self.use_openai_format = config.USE_OPENAI_FORMAT
        self.context = None

    def set_context(self, text: str):
        """
        设置上下文（文章内容）

        Args:
            text: 文章内容
        """
        self.context = text

    def ask(self, question: str) -> str:
        """
        提问

        Args:
            question: 用户问题

        Returns:
            回答
        """
        if not self.context:
            return "请先加载文章内容"

        prompt = config.QA_PROMPT.format(
            text=self.context,
            question=question
        )

        if self.use_openai_format:
            # 智谱 API（OpenAI 格式）
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=2048,
                temperature=0.7
            )
            return response.choices[0].message.content
        else:
            # Anthropic API
            message = self.client.messages.create(
                model=self.model,
                max_tokens=2048,
                messages=[{"role": "user", "content": prompt}]
            )
            return message.content[0].text

    def interactive_mode(self):
        """交互式问答模式"""
        if not self.context:
            print("错误：请先加载文章内容")
            return

        print("\n=== 交互式问答模式 ===")
        print("输入问题，输入 'quit' 或 'exit' 退出\n")

        while True:
            question = input("你的问题: ").strip()

            if question.lower() in ['quit', 'exit', 'q']:
                print("退出问答模式")
                break

            if not question:
                continue

            print("\n回答:")
            answer = self.ask(question)
            print(answer)
            print("\n" + "-" * 50 + "\n")

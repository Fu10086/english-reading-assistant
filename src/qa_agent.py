"""
问答系统模块
基于文章内容的智能问答
"""

from anthropic import Anthropic
import config


class QAAgent:
    """问答助手"""

    def __init__(self, api_key: str = None):
        """
        初始化问答助手

        Args:
            api_key: Claude API Key
        """
        self.api_key = api_key or config.CLAUDE_API_KEY
        if not self.api_key:
            raise ValueError("请设置 CLAUDE_API_KEY 环境变量")

        self.client = Anthropic(
            api_key=self.api_key,
            base_url=config.BASE_URL
        )
        self.model = config.MODEL
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

        message = self.client.messages.create(
            model=self.model,
            max_tokens=2048,
            messages=[
                {"role": "user", "content": prompt}
            ]
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

#!/usr/bin/env python3
"""
使用统计脚本
记录每次使用的 token 消耗和处理的文章数量
"""

import json
import os
from datetime import datetime
from pathlib import Path


class UsageTracker:
    """使用统计追踪器"""

    def __init__(self, stats_file="usage_stats.json"):
        self.stats_file = Path(__file__).parent / stats_file
        self.stats = self._load_stats()

    def _load_stats(self):
        """加载统计数据"""
        if self.stats_file.exists():
            with open(self.stats_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            "total_articles": 0,
            "total_tokens": 0,
            "total_words": 0,
            "sessions": []
        }

    def _save_stats(self):
        """保存统计数据"""
        with open(self.stats_file, 'w', encoding='utf-8') as f:
            json.dump(self.stats, f, indent=2, ensure_ascii=False)

    def record_usage(self, filename, mode, input_tokens, output_tokens, word_count):
        """
        记录一次使用

        Args:
            filename: 处理的文件名
            mode: 处理模式（translate/summary/full等）
            input_tokens: 输入token数
            output_tokens: 输出token数
            word_count: 文章字数
        """
        session = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "filename": filename,
            "mode": mode,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_tokens": input_tokens + output_tokens,
            "word_count": word_count
        }

        self.stats["sessions"].append(session)
        self.stats["total_articles"] += 1
        self.stats["total_tokens"] += session["total_tokens"]
        self.stats["total_words"] += word_count

        self._save_stats()

        print(f"\n✓ 使用记录已保存")
        print(f"  本次消耗: {session['total_tokens']} tokens")
        print(f"  累计文章: {self.stats['total_articles']} 篇")
        print(f"  累计tokens: {self.stats['total_tokens']:,}")

    def show_summary(self):
        """显示统计摘要"""
        print("\n" + "=" * 60)
        print("使用统计摘要")
        print("=" * 60)

        print(f"\n总计:")
        print(f"  处理文章: {self.stats['total_articles']} 篇")
        print(f"  处理字数: {self.stats['total_words']:,} 词")
        print(f"  消耗tokens: {self.stats['total_tokens']:,}")

        if self.stats['total_articles'] > 0:
            avg_tokens = self.stats['total_tokens'] / self.stats['total_articles']
            print(f"  平均每篇: {avg_tokens:.0f} tokens")

        # 按日期统计
        if self.stats['sessions']:
            print(f"\n最近使用:")
            for session in self.stats['sessions'][-5:]:
                print(f"  {session['timestamp']} - {session['filename']}")
                print(f"    模式: {session['mode']}, tokens: {session['total_tokens']}")

    def estimate_daily_usage(self, articles_per_day=10):
        """估算日均使用量"""
        if self.stats['total_articles'] == 0:
            print("\n暂无使用数据，无法估算")
            return

        avg_tokens = self.stats['total_tokens'] / self.stats['total_articles']
        daily_tokens = avg_tokens * articles_per_day
        monthly_tokens = daily_tokens * 30

        print("\n" + "=" * 60)
        print("使用量估算")
        print("=" * 60)
        print(f"\n基于当前数据（平均每篇 {avg_tokens:.0f} tokens）:")
        print(f"  每天处理 {articles_per_day} 篇:")
        print(f"    日消耗: {daily_tokens:,.0f} tokens")
        print(f"    月消耗: {monthly_tokens:,.0f} tokens")
        print(f"\n建议申请额度: {int(monthly_tokens * 1.5):,} tokens/月")


def main():
    """主函数 - 显示统计信息"""
    tracker = UsageTracker()
    tracker.show_summary()
    tracker.estimate_daily_usage()

    print("\n" + "=" * 60)
    print("使用方法")
    print("=" * 60)
    print("""
在 main.py 中集成此脚本，每次处理完文章后自动记录。

或手动记录：
    from usage_tracker import UsageTracker

    tracker = UsageTracker()
    tracker.record_usage(
        filename="article.txt",
        mode="full",
        input_tokens=1000,
        output_tokens=2000,
        word_count=500
    )
""")


if __name__ == "__main__":
    main()

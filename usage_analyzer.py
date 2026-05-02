"""
增强版使用统计工具
提供详细的使用分析和可视化
"""

import json
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict


class UsageAnalyzer:
    """使用统计分析器"""

    def __init__(self, log_file: str = "data/usage_log.json"):
        self.log_file = Path(log_file)
        self.logs = self._load_logs()

    def _load_logs(self):
        """加载使用日志"""
        if not self.log_file.exists():
            return []

        try:
            with open(self.log_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []

    def log_usage(self, mode: str, file_name: str, chars: int, tokens: int = None):
        """记录一次使用"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "mode": mode,
            "file": file_name,
            "chars": chars,
            "tokens": tokens or chars * 0.3  # 估算 token
        }

        self.logs.append(log_entry)

        # 保存
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.log_file, 'w', encoding='utf-8') as f:
            json.dump(self.logs, f, indent=2, ensure_ascii=False)

    def get_summary(self, days: int = 30):
        """获取统计摘要"""
        if not self.logs:
            return {
                "total_files": 0,
                "total_chars": 0,
                "total_tokens": 0,
                "by_mode": {},
                "by_day": {}
            }

        # 过滤最近 N 天的数据
        cutoff = datetime.now() - timedelta(days=days)
        recent_logs = [
            log for log in self.logs
            if datetime.fromisoformat(log["timestamp"]) > cutoff
        ]

        # 统计
        total_files = len(recent_logs)
        total_chars = sum(log["chars"] for log in recent_logs)
        total_tokens = sum(log["tokens"] for log in recent_logs)

        # 按模式统计
        by_mode = defaultdict(lambda: {"count": 0, "chars": 0, "tokens": 0})
        for log in recent_logs:
            mode = log["mode"]
            by_mode[mode]["count"] += 1
            by_mode[mode]["chars"] += log["chars"]
            by_mode[mode]["tokens"] += log["tokens"]

        # 按日期统计
        by_day = defaultdict(lambda: {"count": 0, "tokens": 0})
        for log in recent_logs:
            date = datetime.fromisoformat(log["timestamp"]).date().isoformat()
            by_day[date]["count"] += 1
            by_day[date]["tokens"] += log["tokens"]

        return {
            "total_files": total_files,
            "total_chars": total_chars,
            "total_tokens": int(total_tokens),
            "by_mode": dict(by_mode),
            "by_day": dict(sorted(by_day.items()))
        }

    def print_report(self, days: int = 30):
        """打印统计报告"""
        summary = self.get_summary(days)

        print("\n" + "="*60)
        print(f"📊 使用统计报告（最近 {days} 天）")
        print("="*60)

        print(f"\n📈 总体统计")
        print(f"  处理文章: {summary['total_files']} 篇")
        print(f"  处理字符: {summary['total_chars']:,} 字符")
        print(f"  消耗 Token: {summary['total_tokens']:,}")

        if summary['total_files'] > 0:
            print(f"  平均每篇: {summary['total_tokens'] // summary['total_files']:,} tokens")

        print(f"\n📊 按模式统计")
        for mode, stats in summary['by_mode'].items():
            print(f"  {mode}:")
            print(f"    文章数: {stats['count']}")
            print(f"    Token: {int(stats['tokens']):,}")

        print(f"\n📅 最近使用")
        recent_days = list(summary['by_day'].items())[-7:]  # 最近7天
        for date, stats in recent_days:
            print(f"  {date}: {stats['count']} 篇, {int(stats['tokens']):,} tokens")

        # 预测
        if len(recent_days) > 0:
            avg_daily = sum(s["tokens"] for _, s in recent_days) / len(recent_days)
            print(f"\n🔮 预测")
            print(f"  日均消耗: {int(avg_daily):,} tokens")
            print(f"  月预测: {int(avg_daily * 30):,} tokens")

        print("\n" + "="*60)

    def export_csv(self, output_file: str = "data/usage_report.csv"):
        """导出为 CSV"""
        import csv

        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=["timestamp", "mode", "file", "chars", "tokens"])
            writer.writeheader()
            writer.writerows(self.logs)

        print(f"✅ 已导出到: {output_path}")


if __name__ == "__main__":
    analyzer = UsageAnalyzer()

    # 如果有参数，添加测试数据
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        print("添加测试数据...")
        analyzer.log_usage("summary", "test1.txt", 3000, 9000)
        analyzer.log_usage("translate", "test2.txt", 5000, 15000)
        analyzer.log_usage("note", "test3.txt", 4000, 12000)

    # 显示报告
    analyzer.print_report()

    # 导出 CSV
    if len(sys.argv) > 1 and sys.argv[1] == "export":
        analyzer.export_csv()

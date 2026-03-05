"""
AI Video Market Watch — Haftalık Top 10 Orchestrator

Haftanın günlük verilerini birleştirip Top 10 chart ve haftalık rapor üretir.

Kullanım:
    python scripts/run_weekly.py
    python scripts/run_weekly.py --week 2026-W09
"""

import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from config import DATA_DIR, REPORTS_DIR, CHARTS_DIR
from scorer import score_videos, vmw_level
from report_generator import generate_weekly_chart_html


def _load_week_data(week_label=None):
    """Haftanın tüm günlük veri dosyalarını yükler."""
    if week_label is None:
        now = datetime.now()
        week_label = f"{now.year}-W{now.isocalendar()[1]:02d}"

    # Haftanın tarihlerini hesapla
    year, week_num = int(week_label.split("-W")[0]), int(week_label.split("-W")[1])
    # Pazartesiden başla
    jan1 = datetime(year, 1, 1)
    # ISO hafta 1'in Pazartesi'si
    monday = jan1 + timedelta(days=-jan1.weekday(), weeks=week_num - 1)
    if jan1.weekday() > 3:  # ISO week adjustment
        monday += timedelta(weeks=1)

    dates = [(monday + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7)]

    all_videos = {}
    loaded_days = []

    for date in dates:
        data_file = DATA_DIR / f"all_videos_{date}.json"
        if data_file.exists():
            with open(data_file, "r", encoding="utf-8") as f:
                day_videos = json.load(f)
                for v in day_videos:
                    key = v.get("title", "").lower().strip()[:50]
                    if key:
                        # En yüksek metrikleri tut (en güncel)
                        existing = all_videos.get(key)
                        if existing is None or v.get("view_count", 0) > existing.get("view_count", 0):
                            all_videos[key] = v
                loaded_days.append(date)

    print(f"  Yüklenen günler: {', '.join(loaded_days) or 'Hiçbiri'}")
    print(f"  Toplam benzersiz video: {len(all_videos)}")

    return list(all_videos.values()), week_label, dates


def generate_weekly_report(videos, week_label, dates):
    """Haftalık Markdown rapor üretir."""
    date_range = f"{dates[0]} — {dates[-1]}"

    lines = [
        f"# AI Video Market Watch — Haftalık Top 10",
        f"**Hafta:** {week_label} ({date_range})",
        f"**Toplam Video:** {len(videos)}",
        "",
        "---",
        "",
    ]

    for i, v in enumerate(videos[:10], 1):
        title = v.get("title", "Bilinmiyor")
        vmw = v.get("vmw_score", 0)
        platform = v.get("platform", "?")
        channel = v.get("channel_title", v.get("channel", "?"))
        tools = v.get("ai_tools", [])
        tools_str = ", ".join(tools) if isinstance(tools, list) else str(tools) if tools else "Bilinmiyor"
        views = v.get("view_count", v.get("estimated_views", 0))
        likes = v.get("like_count", 0)
        comments = v.get("comment_count", 0)
        url = v.get("url", "")
        source = "Doğrulanmış" if v.get("metrics_source") == "api" else "Tahmini"

        medal = ""
        if i == 1: medal = "🏆 "
        elif i == 2: medal = "🥈 "
        elif i == 3: medal = "🥉 "

        lines.extend([
            f"### {medal}#{i} — {title}",
            f"- **VMW Score:** {vmw}/100 ({vmw_level(vmw)})",
            f"- **Platform:** {platform}",
            f"- **Kanal/Hesap:** {channel}",
            f"- **AI Araç:** {tools_str}",
            f"- **Metrikler ({source}):**",
            f"  - İzlenme: {views:,}",
            f"  - Beğeni: {likes:,}",
            f"  - Yorum: {comments:,}",
        ])
        if url:
            lines.append(f"- **Link:** {url}")
        lines.append("")

    # Haftalık trendler
    platforms = {}
    tools_count = {}
    for v in videos:
        p = v.get("platform", "?")
        platforms[p] = platforms.get(p, 0) + 1

        vtools = v.get("ai_tools", [])
        if isinstance(vtools, list):
            for t in vtools:
                tools_count[t] = tools_count.get(t, 0) + 1

    lines.extend([
        "---",
        "",
        "## Haftalık Trendler",
        "",
        "### Platform Dağılımı",
        "| Platform | Video Sayısı |",
        "|----------|-------------|",
    ])
    for p, count in sorted(platforms.items(), key=lambda x: x[1], reverse=True):
        lines.append(f"| {p} | {count} |")

    if tools_count:
        lines.extend([
            "",
            "### AI Araç Kullanımı",
            "| Araç | Kullanım |",
            "|------|----------|",
        ])
        for t, count in sorted(tools_count.items(), key=lambda x: x[1], reverse=True)[:10]:
            lines.append(f"| {t} | {count} |")

    lines.extend([
        "",
        "---",
        "",
        f"*VMW Agent — Haftalık Rapor*",
        f"*{week_label}*",
    ])

    output_dir = REPORTS_DIR / "weekly"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{week_label}.md"

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"[Rapor] Haftalık rapor → {output_path}")
    return output_path


def run_weekly(week_label=None):
    """Haftalık pipeline."""
    print(f"\n{'='*60}")
    print(f"  AI VIDEO MARKET WATCH — HAFTALIK TOP 10")
    print(f"{'='*60}\n")

    videos, week_label, dates = _load_week_data(week_label)

    if not videos:
        print("  [UYARI] Bu hafta için veri bulunamadı. Önce günlük tarama çalıştırın.")
        return

    # Skorla ve sırala
    scored = score_videos(videos)

    # Rapor ve chart üret
    report_path = generate_weekly_report(scored, week_label, dates)
    chart_path = generate_weekly_chart_html(scored, week_label)

    print(f"\n{'='*60}")
    print(f"  HAFTALIK RAPOR TAMAMLANDI")
    print(f"{'='*60}")
    print(f"  Hafta: {week_label}")
    print(f"  Video sayısı: {len(scored)}")
    print(f"  Rapor: {report_path}")
    print(f"  Chart: {chart_path}")

    if scored:
        print(f"\n  Top 3:")
        for i, v in enumerate(scored[:3], 1):
            print(f"    #{i} [{v.get('vmw_score', 0)}] {v.get('title', '?')[:50]}")


# --- CLI ---
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="VMW Haftalık Top 10")
    parser.add_argument("--week", type=str, default=None, help="Hafta etiketi (YYYY-WNN)")

    args = parser.parse_args()
    run_weekly(week_label=args.week)

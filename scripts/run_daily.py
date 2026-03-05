"""
AI Video Market Watch — Günlük Tarama Orchestrator

YouTube Data API ile AI video arama + metrik toplama.
Opsiyonel: Perplexity ile ek keşif.

Kullanım:
    python scripts/run_daily.py
    python scripts/run_daily.py --date 2026-02-25
    python scripts/run_daily.py --with-discovery    # Perplexity keşfi de çalıştır
"""

import json
import sys
from datetime import datetime
from pathlib import Path

# Script klasöründen import yapabilmek için
sys.path.insert(0, str(Path(__file__).parent))

from config import DATA_DIR
from youtube_metrics import search_ai_videos, get_video_metrics, save_results, detect_ai_tools, classify_video_type
from scorer import score_videos
from report_generator import generate_daily_report, generate_daily_report_html
from email_sender import send_daily_report_email


def merge_videos(youtube_results, discovery_results=None):
    """
    Farklı kaynaklardan gelen videoları birleştirir ve deduplication yapar.
    YouTube (kesin metrik) her zaman öncelikli.
    """
    all_videos = []
    seen = set()  # title.lower() bazlı dedup

    # YouTube (kesin metrik) öncelikli
    for v in youtube_results:
        key = v.get("title", "").lower().strip()[:50]
        if key and key not in seen:
            seen.add(key)
            all_videos.append(v)

    # Perplexity keşif (varsa)
    if discovery_results:
        for v in discovery_results:
            key = v.get("title", "").lower().strip()[:50]
            if key and key not in seen:
                seen.add(key)
                all_videos.append(v)

    return all_videos


def run_daily(date=None, with_discovery=False):
    """Günlük tarama pipeline'ı."""
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")

    steps = 3 if with_discovery else 2

    print(f"\n{'='*60}")
    print(f"  AI VIDEO MARKET WATCH — GÜNLÜK TARAMA")
    print(f"  Tarih: {date}")
    print(f"{'='*60}")

    youtube_results = []
    discovery_results = []

    # Adım 1: YouTube Araması
    print(f"\n[1/{steps}] YouTube AI Video Araması...")
    try:
        search_results = search_ai_videos(days_back=7)
        if search_results:
            video_ids = [v["video_id"] for v in search_results]
            metrics = get_video_metrics(video_ids)
            # Metrikleri birleştir
            metrics_map = {m["video_id"]: m for m in metrics}
            for v in search_results:
                m = metrics_map.get(v["video_id"], {})
                v.update({
                    "view_count": m.get("view_count", 0),
                    "like_count": m.get("like_count", 0),
                    "comment_count": m.get("comment_count", 0),
                    "duration": m.get("duration", ""),
                    "tags": m.get("tags", []),
                    "url": m.get("url", f"https://www.youtube.com/watch?v={v['video_id']}"),
                    "metrics_source": "api",
                })
            youtube_results = search_results
            save_results(youtube_results, f"youtube_{date}.json")
    except Exception as e:
        print(f"  [HATA] YouTube aramasında hata: {e}")

    # Adım 2 (opsiyonel): Perplexity Keşif
    if with_discovery:
        print(f"\n[2/{steps}] Perplexity AI Video Keşfi...")
        try:
            from discovery import discover_ai_videos, save_candidates
            discovery_results = discover_ai_videos()
            if discovery_results:
                save_candidates(discovery_results, f"discovery_{date}.json")
        except Exception as e:
            print(f"  [HATA] Perplexity keşfinde hata: {e}")

    # Birleştir
    all_videos = merge_videos(youtube_results, discovery_results)
    print(f"\n  Toplam: {len(all_videos)} benzersiz video")

    # AI araç tespiti ve video sınıflandırma
    for v in all_videos:
        if not v.get("ai_tools"):
            v["ai_tools"] = detect_ai_tools(v)
        v["video_type"] = classify_video_type(v)

    # Sınıflandırma özeti
    ai_made = [v for v in all_videos if v["video_type"] in ("ai_made", "ai_tutorial")]
    ai_about = [v for v in all_videos if v["video_type"] == "ai_about"]
    uncertain = [v for v in all_videos if v["video_type"] == "uncertain"]
    print(f"  Sınıflandırma: {len(ai_made)} yapım | {len(ai_about)} haber/tartışma | {len(uncertain)} belirsiz")

    # Skorla ve raporla
    step_num = steps
    print(f"\n[{step_num}/{steps}] VMW Score hesaplanıyor ve rapor üretiliyor...")
    scored_videos = score_videos(all_videos)

    # Rapor için: AI yapım videoları önce, belirsizler sonra, haber/tartışma en sona
    type_order = {"ai_made": 0, "ai_tutorial": 1, "uncertain": 2, "ai_about": 3}
    scored_videos.sort(key=lambda v: (type_order.get(v.get("video_type", "uncertain"), 2), -v.get("vmw_score", 0)))

    report_path = generate_daily_report(scored_videos, date=date)
    html_path = generate_daily_report_html(scored_videos, date=date)

    # Email gönder
    print(f"\n  Email gönderiliyor...")
    send_daily_report_email(html_path, date=date)

    # Tüm verileri kaydet
    all_data_path = DATA_DIR / f"all_videos_{date}.json"
    with open(all_data_path, "w", encoding="utf-8") as f:
        json.dump(scored_videos, f, ensure_ascii=False, indent=2, default=str)

    # Özet
    print(f"\n{'='*60}")
    print(f"  GÜNLÜK TARAMA TAMAMLANDI")
    print(f"{'='*60}")
    print(f"  Toplam video: {len(scored_videos)}")
    print(f"  YouTube (kesin): {len(youtube_results)}")
    if discovery_results:
        print(f"  Perplexity keşif: {len(discovery_results)}")
    print(f"  AI yapım: {len(ai_made)} | Haber: {len(ai_about)} | Belirsiz: {len(uncertain)}")
    print(f"  Rapor (MD):   {report_path}")
    print(f"  Rapor (HTML): {html_path}")
    print(f"  Veri: {all_data_path}")

    if scored_videos:
        print(f"\n  Top 3:")
        for i, v in enumerate(scored_videos[:3], 1):
            tools = ", ".join(v.get("ai_tools", [])) or "?"
            print(f"    #{i} [{v.get('vmw_score', 0)}] {v.get('title', '?')[:45]} ({tools})")

    return scored_videos


# --- CLI ---
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="VMW Günlük Tarama")
    parser.add_argument("--date", type=str, default=None, help="Rapor tarihi (YYYY-MM-DD)")
    parser.add_argument("--with-discovery", action="store_true", help="Perplexity keşfini de çalıştır")

    args = parser.parse_args()
    run_daily(date=args.date, with_discovery=args.with_discovery)

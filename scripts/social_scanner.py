"""
AI Video Market Watch — Social Scanner Module

X, TikTok, Instagram için Perplexity tabanlı metrik tahmini.
Kullanım:
    from social_scanner import scan_social_platforms
    results = scan_social_platforms()
"""

import json
from datetime import datetime

from config import SOCIAL_QUERIES, DATA_DIR
from discovery import _call_perplexity, _parse_video_candidates


def scan_platform(platform, query=None):
    """
    Tek bir platform için Perplexity proxy taraması.

    Args:
        platform: "x" | "tiktok" | "instagram"
        query: Özel sorgu (opsiyonel)

    Returns:
        list[dict]: Video adayları
    """
    if query is None:
        query = SOCIAL_QUERIES.get(platform, "")

    if not query:
        print(f"  [{platform}] Sorgu tanımlı değil, atlanıyor.")
        return []

    system_prompt = (
        f"Sen Türkiye'deki {platform.upper()} platformunda viral olan AI videoları takip eden bir analistsin. "
        f"Son 7 günde {platform}'da Türkiye'de en çok izlenen/paylaşılan, yapay zeka araçları (Seedance, Kling, Sora, "
        "Runway, Veo, Minimax, Pika, Luma, Midjourney vb.) kullanılarak ÜRETİLMİŞ videoları listele. "
        "AI hakkında haber değil, AI ile YAPILMIŞ içerikler. "
        "Yanıtını aşağıdaki JSON array formatında ver, başka açıklama ekleme:\n"
        '[{"title":"...","platform":"' + platform + '","channel":"@hesap","ai_tools":["Seedance"],"estimated_views":150000,"url":"https://..."}]'
    )

    print(f"  [{platform.upper()}] Taranıyor...")
    raw = _call_perplexity(query, system_prompt=system_prompt)

    if not raw:
        print(f"  [{platform.upper()}] Yanıt alınamadı.")
        return []

    candidates = _parse_video_candidates(raw)

    # Platform bilgisini ekle
    for c in candidates:
        c["platform"] = platform
        c["metrics_source"] = "perplexity"
        c["scan_date"] = datetime.now().isoformat()

    print(f"  [{platform.upper()}] {len(candidates)} video adayı bulundu.")
    return candidates


def scan_social_platforms(platforms=None):
    """
    Tüm sosyal medya platformlarını tarar.

    Returns:
        dict: {platform: list[dict]} — platform bazlı sonuçlar
    """
    if platforms is None:
        platforms = ["x", "tiktok", "instagram"]

    print(f"\n{'='*60}")
    print(f"Sosyal Medya Taraması — {', '.join(p.upper() for p in platforms)}")
    print(f"{'='*60}\n")

    results = {}
    total = 0

    for platform in platforms:
        candidates = scan_platform(platform)
        results[platform] = candidates
        total += len(candidates)

    print(f"\n[Sosyal] Toplam {total} video adayı ({len(platforms)} platform).")
    return results


def save_social_results(results, filename="social_scan_latest.json"):
    """Sonuçları JSON olarak kaydet."""
    output_path = DATA_DIR / filename
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2, default=str)
    print(f"[Kayıt] Sonuçlar → {output_path}")


# --- CLI ---
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Social Media AI Video Scanner")
    parser.add_argument("--platform", type=str, choices=["x", "tiktok", "instagram", "all"], default="all")

    args = parser.parse_args()

    if args.platform == "all":
        results = scan_social_platforms()
    else:
        results = scan_social_platforms(platforms=[args.platform])

    for platform, candidates in results.items():
        if candidates:
            print(f"\n--- {platform.upper()} ---")
            for i, c in enumerate(candidates, 1):
                print(f"  #{i} {c['title'][:60]}")
                if c.get("channel"):
                    print(f"     👤 {c['channel']}")
                if c.get("estimated_views"):
                    print(f"     👁 ~{c['estimated_views']:,} (tahmini)")

    save_social_results(results)

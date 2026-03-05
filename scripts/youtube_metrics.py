"""
AI Video Market Watch — YouTube Data API Module

YouTube'dan AI video arama ve kesin metrik toplama.
Kullanım:
    from youtube_metrics import search_ai_videos, get_video_metrics

    # Keyword bazlı arama
    videos = search_ai_videos(keywords=["yapay zeka video"], days_back=7)

    # Bilinen video ID'lerinin metriklerini çek
    metrics = get_video_metrics(["dQw4w9WgXcQ", "abc123"])
"""

import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from config import (
    YOUTUBE_API_KEY,
    YOUTUBE_REGION,
    YOUTUBE_MAX_RESULTS,
    YOUTUBE_SEARCH_ORDER,
    KEYWORDS_TR,
    KEYWORDS_TOOLS,
    DATA_DIR,
    AI_TOOLS,
)


# Tüm AI araç isimlerini küçük harfle bir set'e topla (hızlı arama için)
_ALL_TOOLS = {}
for _category, _tools in AI_TOOLS.items():
    for _tool in _tools:
        _ALL_TOOLS[_tool.lower()] = _tool  # "seedance" → "Seedance"

# Ek eşleştirmeler (kısaltmalar, alternatif yazımlar)
_TOOL_ALIASES = {
    "seed dance": "Seedance", "seedance pro": "Seedance",
    "seedance 2": "Seedance", "seedance 2.0": "Seedance",
    "dall-e 3": "DALL-E", "dalle": "DALL-E", "dall-e": "DALL-E",
    "midjourney v6": "Midjourney", "midjourney v7": "Midjourney", "mj": "Midjourney",
    "stable diffusion": "Stable Diffusion", "sd": "Stable Diffusion", "sdxl": "Stable Diffusion",
    "runway gen-3": "Runway", "runway gen3": "Runway", "runway gen-2": "Runway", "runway ml": "Runway",
    "kling 1.6": "Kling", "kling ai": "Kling", "kling 2": "Kling",
    "sora ai": "Sora", "openai sora": "Sora",
    "google veo": "Veo", "veo 2": "Veo", "veo 3": "Veo", "veo2": "Veo", "veo3": "Veo",
    "minimax hailuo": "Minimax", "hailuo": "Minimax", "hailuo ai": "Minimax",
    "pika labs": "Pika", "pika ai": "Pika",
    "luma dream machine": "Luma", "dream machine": "Luma", "luma ai": "Luma",
    "haiper ai": "Haiper",
    "wan ai": "Wan", "wan 2.1": "Wan", "wan2.1": "Wan",
    "pixverse ai": "PixVerse",
    "suno ai": "Suno", "suno v4": "Suno",
    "udio ai": "Udio",
    "elevenlabs": "ElevenLabs", "eleven labs": "ElevenLabs",
    "topaz ai": "Topaz", "topaz video ai": "Topaz",
    "capcut ai": "CapCut AI",
    "magnific ai": "Magnific AI", "magnific": "Magnific AI",
    "chatgpt": "ChatGPT", "gpt-4": "ChatGPT", "gpt-4o": "ChatGPT",
    "gemini": "Gemini", "google gemini": "Gemini",
    "flux ai": "Flux", "flux 1.1": "Flux",
    "ideogram ai": "Ideogram",
    "imagen": "Imagen", "google imagen": "Imagen",
}


def detect_ai_tools(video):
    """Video başlık, açıklama ve tag'lerinden kullanılan AI araçlarını tespit et."""
    text_parts = [
        video.get("title", ""),
        video.get("description", ""),
    ]
    tags = video.get("tags", [])
    if isinstance(tags, list):
        text_parts.extend(tags)

    combined = " ".join(str(p) for p in text_parts).lower()
    found = set()

    # Önce alias'ları kontrol et (daha spesifik eşleşmeler)
    for alias, canonical in _TOOL_ALIASES.items():
        if alias in combined:
            found.add(canonical)

    # Sonra direkt araç isimleri
    for tool_lower, tool_canonical in _ALL_TOOLS.items():
        if tool_lower in combined:
            found.add(tool_canonical)

    # False positive temizliği
    # "Sora" = Mobile Legends karakter adı — AI bağlamında değilse kaldır
    if "Sora" in found:
        sora_false = any(kw in combined for kw in [
            "mobile legends", "mlbb", "moonton", "emblem", "build sora",
            "sora best build", "sora exp lane", "sora gameplay", "win rate",
        ])
        if sora_false:
            found.discard("Sora")

    # "Runway" = moda podyumu bağlamı — AI değilse kaldır
    if "Runway" in found:
        runway_false = any(kw in combined for kw in [
            "fashion week", "fashion show", "runway look", "bafta", "met gala",
            "red carpet", "runway walk", "fashion runway",
        ])
        if runway_false:
            found.discard("Runway")

    # "Wan" = kısa kelime, çok fazla false positive — sadece "wan ai", "wan 2.1" vb. kabul et
    if "Wan" in found:
        wan_valid = any(kw in combined for kw in [
            "wan ai", "wan 2.1", "wan2.1", "wan video ai", "wan model",
        ])
        if not wan_valid:
            found.discard("Wan")

    # "Veo" = kısa kelime — sadece "veo 2", "veo 3", "google veo" vb. kabul et
    if "Veo" in found:
        veo_valid = any(kw in combined for kw in [
            "google veo", "veo 2", "veo 3", "veo2", "veo3", "veo ai",
            "veo video", "veo ile",
        ])
        if not veo_valid:
            found.discard("Veo")

    return sorted(found)


def classify_video_type(video):
    """
    Videonun AI ile yapılmış mı yoksa AI hakkında mı olduğunu sınıfla.

    Returns:
        str: "ai_made" | "ai_about" | "ai_tutorial" | "uncertain"
    """
    title = video.get("title", "").lower()
    desc = video.get("description", "").lower()
    combined = title + " " + desc

    # AI ile YAPILMIŞ video sinyalleri
    made_signals = [
        "made with", "created with", "generated with", "yapıldı", "yapılmış",
        "ile yapılan", "ile yapıldı", "ai short film", "ai film", "ai video",
        "#aivideo", "#aifilm", "#aianimasyon", "#aiileyapıldı",
        "ai generated", "ai-generated", "yapay zeka ile üretilmiş",
        "ai animation", "ai music video", "ai commercial",
    ]

    # AI HAKKINDA konuşan / haber video sinyalleri
    about_signals = [
        "news", "haber", "nasıl kullanılır", "tutorial", "how to use",
        "nedir", "what is", "review", "inceleme", "comparison", "karşılaştırma",
        "vs", "versus", "impact", "addresses", "summit", "conference",
        "interview", "söyleşi", "podcast", "react", "reacting to",
        "explained", "anlatıyorum",
    ]

    # Tutorial sinyalleri
    tutorial_signals = [
        "how to make", "nasıl yapılır", "tutorial", "step by step",
        "guide", "rehber", "kılavuz", "how to create", "tips",
        "masterclass", "course", "ders",
    ]

    made_count = sum(1 for s in made_signals if s in combined)
    about_count = sum(1 for s in about_signals if s in combined)
    tutorial_count = sum(1 for s in tutorial_signals if s in combined)

    ai_tools = video.get("ai_tools", [])

    # AI aracı tespit edildiyse ve yapılmış sinyali varsa → ai_made
    if ai_tools and made_count > 0:
        return "ai_made"

    # Tutorial sinyali güçlüyse
    if tutorial_count > 0 and ai_tools:
        return "ai_tutorial"

    # AI hakkında konuşan video
    if about_count > made_count and about_count > 0:
        return "ai_about"

    # AI aracı tespit edildi ama net değil
    if ai_tools:
        return "ai_made"

    return "uncertain"


def _get_youtube_client():
    if not YOUTUBE_API_KEY:
        print("[HATA] YOUTUBE_API_KEY .env dosyasında tanımlı değil.")
        sys.exit(1)
    return build("youtube", "v3", developerKey=YOUTUBE_API_KEY)


def search_ai_videos(keywords=None, days_back=7, max_per_keyword=10):
    """
    YouTube'da AI video keyword'leriyle arama yapar.

    Returns:
        list[dict]: Her video için {video_id, title, channel_title, channel_id,
                     published_at, description, thumbnail_url}
    """
    youtube = _get_youtube_client()
    if keywords is None:
        keywords = KEYWORDS_TR[:5] + KEYWORDS_TOOLS[:5]  # Quota koruma: 10 arama

    published_after = (datetime.now(timezone.utc) - timedelta(days=days_back)).isoformat()

    seen_ids = set()
    results = []

    for kw in keywords:
        try:
            response = youtube.search().list(
                q=kw,
                part="snippet",
                type="video",
                regionCode=YOUTUBE_REGION,
                publishedAfter=published_after,
                order=YOUTUBE_SEARCH_ORDER,
                maxResults=max_per_keyword,
                relevanceLanguage="tr",
            ).execute()

            for item in response.get("items", []):
                vid = item["id"]["videoId"]
                if vid in seen_ids:
                    continue
                seen_ids.add(vid)

                snippet = item["snippet"]
                results.append({
                    "video_id": vid,
                    "title": snippet["title"],
                    "channel_title": snippet["channelTitle"],
                    "channel_id": snippet["channelId"],
                    "published_at": snippet["publishedAt"],
                    "description": snippet.get("description", "")[:300],
                    "thumbnail_url": snippet.get("thumbnails", {}).get("high", {}).get("url", ""),
                    "search_keyword": kw,
                    "platform": "youtube",
                })

            print(f"  [YouTube] '{kw}' → {len(response.get('items', []))} sonuç")

        except HttpError as e:
            print(f"  [YouTube HATA] '{kw}' aramasında hata: {e}")
            if "quotaExceeded" in str(e):
                print("  [YouTube] Günlük quota aşıldı, arama durduruluyor.")
                break

    print(f"[YouTube] Toplam {len(results)} benzersiz video bulundu.")
    return results


def get_video_metrics(video_ids):
    """
    Video ID listesi için kesin metrikleri çeker.

    Args:
        video_ids: list[str] — YouTube video ID'leri

    Returns:
        list[dict]: Her video için {video_id, title, channel_title, channel_id,
                     published_at, view_count, like_count, comment_count,
                     duration, tags, category_id, url}
    """
    youtube = _get_youtube_client()
    results = []

    # YouTube API bir seferde max 50 video kabul eder
    for i in range(0, len(video_ids), 50):
        batch = video_ids[i:i+50]
        ids_str = ",".join(batch)

        try:
            response = youtube.videos().list(
                id=ids_str,
                part="snippet,statistics,contentDetails",
            ).execute()

            for item in response.get("items", []):
                stats = item.get("statistics", {})
                snippet = item["snippet"]
                content = item.get("contentDetails", {})

                results.append({
                    "video_id": item["id"],
                    "title": snippet["title"],
                    "channel_title": snippet["channelTitle"],
                    "channel_id": snippet["channelId"],
                    "published_at": snippet["publishedAt"],
                    "description": snippet.get("description", "")[:500],
                    "tags": snippet.get("tags", []),
                    "category_id": snippet.get("categoryId", ""),
                    "thumbnail_url": snippet.get("thumbnails", {}).get("high", {}).get("url", ""),
                    "view_count": int(stats.get("viewCount", 0)),
                    "like_count": int(stats.get("likeCount", 0)),
                    "comment_count": int(stats.get("commentCount", 0)),
                    "duration": content.get("duration", ""),
                    "url": f"https://www.youtube.com/watch?v={item['id']}",
                    "platform": "youtube",
                    "metrics_source": "api",  # Kesin veri
                })

        except HttpError as e:
            print(f"  [YouTube HATA] Metrik çekiminde hata: {e}")

    print(f"[YouTube] {len(results)} video için metrikler alındı.")
    return results


def get_channel_info(channel_ids):
    """
    Kanal ID listesi için bilgileri çeker.

    Returns:
        list[dict]: {channel_id, title, subscriber_count, video_count, description}
    """
    youtube = _get_youtube_client()
    results = []

    for i in range(0, len(channel_ids), 50):
        batch = channel_ids[i:i+50]
        ids_str = ",".join(batch)

        try:
            response = youtube.channels().list(
                id=ids_str,
                part="snippet,statistics",
            ).execute()

            for item in response.get("items", []):
                stats = item.get("statistics", {})
                snippet = item["snippet"]
                results.append({
                    "channel_id": item["id"],
                    "title": snippet["title"],
                    "subscriber_count": int(stats.get("subscriberCount", 0)),
                    "video_count": int(stats.get("videoCount", 0)),
                    "description": snippet.get("description", "")[:300],
                })

        except HttpError as e:
            print(f"  [YouTube HATA] Kanal bilgisi çekiminde hata: {e}")

    return results


def save_results(data, filename):
    """Sonuçları JSON olarak kaydet."""
    output_path = DATA_DIR / filename
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2, default=str)
    print(f"[Kayıt] {len(data)} kayıt → {output_path}")


# --- CLI ---
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="YouTube AI Video Metrics")
    parser.add_argument("--search", action="store_true", help="Keyword bazlı arama yap")
    parser.add_argument("--video-ids", type=str, help="Virgülle ayrılmış video ID'leri için metrik çek")
    parser.add_argument("--days", type=int, default=7, help="Kaç gün geriye bak (default: 7)")
    parser.add_argument("--keywords", type=str, help="Özel keyword'ler (virgülle ayrılmış)")

    args = parser.parse_args()

    if args.video_ids:
        ids = [vid.strip() for vid in args.video_ids.split(",")]
        print(f"\n{'='*60}")
        print(f"YouTube Metrik Toplama — {len(ids)} video")
        print(f"{'='*60}\n")
        metrics = get_video_metrics(ids)
        for v in metrics:
            print(f"\n  {v['title']}")
            print(f"  👁 {v['view_count']:,} izlenme | 👍 {v['like_count']:,} beğeni | 💬 {v['comment_count']:,} yorum")
            print(f"  📅 {v['published_at'][:10]} | 🔗 {v['url']}")
        save_results(metrics, "youtube_metrics_latest.json")

    elif args.search:
        keywords = None
        if args.keywords:
            keywords = [k.strip() for k in args.keywords.split(",")]

        print(f"\n{'='*60}")
        print(f"YouTube AI Video Araması — Son {args.days} gün")
        print(f"{'='*60}\n")

        videos = search_ai_videos(keywords=keywords, days_back=args.days)

        if videos:
            # Bulunan videoların metriklerini de çek
            video_ids = [v["video_id"] for v in videos]
            metrics = get_video_metrics(video_ids)

            # Metrikleri birleştir
            metrics_map = {m["video_id"]: m for m in metrics}
            for v in videos:
                m = metrics_map.get(v["video_id"], {})
                v.update({
                    "view_count": m.get("view_count", 0),
                    "like_count": m.get("like_count", 0),
                    "comment_count": m.get("comment_count", 0),
                })

            # Sırala ve göster
            videos.sort(key=lambda x: x.get("view_count", 0), reverse=True)
            print(f"\n{'='*60}")
            print(f"Sonuçlar (izlenmeye göre sıralı):")
            print(f"{'='*60}")
            for i, v in enumerate(videos[:20], 1):
                print(f"\n  #{i} {v['title'][:70]}")
                print(f"     👁 {v.get('view_count', 0):,} | 👍 {v.get('like_count', 0):,} | 💬 {v.get('comment_count', 0):,}")
                print(f"     📺 {v['channel_title']} | 📅 {v['published_at'][:10]}")
                print(f"     🔍 Keyword: {v['search_keyword']}")

            save_results(videos, "youtube_search_latest.json")

    else:
        print("Kullanım:")
        print("  python youtube_metrics.py --search                          # Keyword araması")
        print("  python youtube_metrics.py --search --days 3                 # Son 3 gün")
        print("  python youtube_metrics.py --search --keywords 'sora,kling'  # Özel keyword")
        print("  python youtube_metrics.py --video-ids 'ID1,ID2,ID3'         # Metrik çek")

"""
AI Video Market Watch — VMW Score Calculator

Her video için 0-100 arası VMW (Video Market Watch) Score hesaplar.
Kullanım:
    from scorer import calculate_vmw_score, score_videos
    scored = score_videos(video_list)
"""

import math

from config import VMW_WEIGHTS, VIEW_TIERS, AI_TOOLS


def _view_score(view_count):
    """Görüntülenme sayısına göre puan (0-15)."""
    for threshold, score in VIEW_TIERS:
        if view_count >= threshold:
            return score
    return 0


def _engagement_rate(video):
    """Etkileşim oranı hesapla."""
    views = video.get("view_count", 0) or video.get("estimated_views", 0)
    if views == 0:
        return 0
    likes = video.get("like_count", 0)
    comments = video.get("comment_count", 0)
    shares = video.get("share_count", 0)
    return (likes + comments * 2 + shares * 3) / views


def _platform_count(video):
    """Video kaç platformda mevcut."""
    platforms = video.get("platforms", [])
    if isinstance(platforms, list) and platforms:
        return len(platforms)
    return 1


def _ai_complexity(video):
    """Kullanılan AI araçlarının karmaşıklık skoru (0-6)."""
    tools = video.get("ai_tools", [])
    if isinstance(tools, str):
        tools = [tools]
    if not tools:
        return 2  # Bilinmiyor ama AI olduğu doğrulanmış → orta puan

    tool_count = len(tools)
    # Video üretim aracı kullanılmış mı?
    has_video_tool = any(t in AI_TOOLS["video"] for t in tools)
    has_image_tool = any(t in AI_TOOLS["image"] for t in tools)
    has_audio_tool = any(t in AI_TOOLS["audio"] for t in tools)

    score = min(tool_count, 3)  # Max 3 puan araç sayısından
    if has_video_tool:
        score += 1
    if has_video_tool and has_image_tool:
        score += 1
    if has_audio_tool:
        score += 1

    return min(score, 6)


def calculate_vmw_score(video):
    """
    Tek bir video için VMW Score hesaplar.

    Args:
        video: dict — video bilgileri (view_count, like_count, comment_count, ai_tools, vb.)

    Returns:
        dict: {reach, engagement, buzz, innovation, total, breakdown}
    """
    views = video.get("view_count", 0) or video.get("estimated_views", 0)

    # --- REACH (0-30) ---
    reach_views = _view_score(views)  # 0-15

    # Hız: Eğer son 3 günde yayınlandıysa bonus
    velocity = 0
    days_old = video.get("days_since_publish", 30)
    if days_old <= 1:
        velocity = 9
    elif days_old <= 3:
        velocity = 7
    elif days_old <= 7:
        velocity = 5
    elif days_old <= 14:
        velocity = 3
    elif days_old <= 30:
        velocity = 1

    cross_platform = min(_platform_count(video) * 2, 6)  # 0-6

    reach = reach_views + velocity + cross_platform
    reach = min(reach, 30)

    # --- ENGAGEMENT (0-30) ---
    eng_rate = _engagement_rate(video)

    # Etkileşim oranına göre puan (0-12)
    if eng_rate >= 0.10:
        rate_score = 12
    elif eng_rate >= 0.05:
        rate_score = 10
    elif eng_rate >= 0.03:
        rate_score = 8
    elif eng_rate >= 0.01:
        rate_score = 5
    elif eng_rate > 0:
        rate_score = 2
    else:
        rate_score = 0

    # Yorum kalitesi (tahmini — yorum sayısına göre proxy)
    comment_count = video.get("comment_count", 0)
    if comment_count >= 1000:
        comment_quality = 9
    elif comment_count >= 500:
        comment_quality = 7
    elif comment_count >= 100:
        comment_quality = 5
    elif comment_count >= 20:
        comment_quality = 3
    elif comment_count > 0:
        comment_quality = 1
    else:
        comment_quality = 0

    # Paylaşım/kaydetme (genellikle erişilemez → yorum sayısından proxy)
    share_save = min(int(comment_count * 0.015), 9)

    engagement = rate_score + comment_quality + share_save
    engagement = min(engagement, 30)

    # --- BUZZ (0-25) ---
    buzz_social = video.get("buzz_social", 0)     # Manuel veya Perplexity'den
    buzz_news = video.get("buzz_news", 0)         # Manuel veya Perplexity'den
    buzz_community = video.get("buzz_community", 0)

    # Eğer buzz skorları yoksa, view count'tan tahmin et
    if buzz_social == 0 and views > 0:
        buzz_social = min(int(math.log10(max(views, 1)) * 1.5), 10)
    if buzz_news == 0 and video.get("news_mentions", 0) > 0:
        buzz_news = min(video["news_mentions"] * 3, 8)

    buzz = buzz_social + buzz_news + buzz_community
    buzz = min(buzz, 25)

    # --- INNOVATION (0-15) ---
    technical = _ai_complexity(video)  # 0-6

    creativity = video.get("creativity_score", 3)  # Manuel veya default 3/5
    creativity = min(int(creativity), 5)

    quality = video.get("quality_score", 2)  # Manuel veya default 2/4
    quality = min(int(quality), 4)

    innovation = technical + creativity + quality
    innovation = min(innovation, 15)

    # --- TOPLAM ---
    total = reach + engagement + buzz + innovation

    return {
        "reach": reach,
        "engagement": engagement,
        "buzz": buzz,
        "innovation": innovation,
        "total": min(total, 100),
        "breakdown": {
            "reach_views": reach_views,
            "reach_velocity": velocity,
            "reach_cross_platform": cross_platform,
            "eng_rate": round(eng_rate, 4),
            "eng_rate_score": rate_score,
            "eng_comment_quality": comment_quality,
            "eng_share_save": share_save,
            "buzz_social": buzz_social,
            "buzz_news": buzz_news,
            "buzz_community": buzz_community,
            "innov_technical": technical,
            "innov_creativity": creativity,
            "innov_quality": quality,
        },
    }


def score_videos(videos):
    """
    Video listesini skorlar ve sıralar.

    Returns:
        list[dict]: VMW Score eklenmiş ve sıralanmış video listesi
    """
    for video in videos:
        score = calculate_vmw_score(video)
        video["vmw_score"] = score["total"]
        video["vmw_reach"] = score["reach"]
        video["vmw_engagement"] = score["engagement"]
        video["vmw_buzz"] = score["buzz"]
        video["vmw_innovation"] = score["innovation"]
        video["vmw_breakdown"] = score["breakdown"]

    videos.sort(key=lambda v: v.get("vmw_score", 0), reverse=True)
    return videos


def vmw_level(score):
    """VMW Score'a göre seviye belirleme."""
    if score >= 90:
        return "Fenomen"
    elif score >= 75:
        return "Hit"
    elif score >= 60:
        return "Başarılı"
    elif score >= 45:
        return "İyi"
    elif score >= 30:
        return "Ortalama"
    else:
        return "Düşük"


# --- CLI ---
if __name__ == "__main__":
    # Örnek test
    test_video = {
        "title": "Aşk-ı Memnu Kung Fu Finali",
        "view_count": 2_500_000,
        "like_count": 85_000,
        "comment_count": 3_200,
        "ai_tools": ["Seedance"],
        "days_since_publish": 9,
        "platforms": ["instagram", "x", "tiktok"],
        "news_mentions": 8,
        "creativity_score": 4,
        "quality_score": 3,
    }

    score = calculate_vmw_score(test_video)
    print(f"\n{'='*60}")
    print(f"VMW Score Test: {test_video['title']}")
    print(f"{'='*60}")
    print(f"\n  Reach:      {score['reach']}/30")
    print(f"  Engagement: {score['engagement']}/30")
    print(f"  Buzz:       {score['buzz']}/25")
    print(f"  Innovation: {score['innovation']}/15")
    print(f"  ─────────────────────")
    print(f"  TOPLAM:     {score['total']}/100 ({vmw_level(score['total'])})")
    print(f"\n  Detay: {json.dumps(score['breakdown'], indent=2)}" if False else "")

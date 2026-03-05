"""
AI Video Market Watch — Config & Constants
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
SCRIPTS_DIR = PROJECT_ROOT / "scripts"
DATA_DIR = PROJECT_ROOT / "data"
REPORTS_DIR = PROJECT_ROOT / "reports"
CHARTS_DIR = PROJECT_ROOT / "charts"
INSIGHTS_DIR = PROJECT_ROOT / "insights"

# Load .env
load_dotenv(PROJECT_ROOT / ".env")

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY", "")
PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY", "")

# Email (Gmail SMTP)
EMAIL_SENDER = os.getenv("EMAIL_SENDER", "yucezerey@gmail.com")
EMAIL_RECIPIENT = os.getenv("EMAIL_RECIPIENT", "yucezerey@gmail.com")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD", "")

# Perplexity API
PERPLEXITY_BASE_URL = "https://api.perplexity.ai/chat/completions"
PERPLEXITY_MODEL = "sonar"
PERPLEXITY_MAX_TOKENS = 2000
PERPLEXITY_TEMPERATURE = 0.3  # Lower for factual accuracy

# YouTube API
YOUTUBE_REGION = "TR"
YOUTUBE_MAX_RESULTS = 10
YOUTUBE_SEARCH_ORDER = "viewCount"  # relevance, date, rating, viewCount

# Search Keywords
KEYWORDS_TR = [
    "yapay zeka video",
    "yapay zeka ile yapılan video",
    "AI video Türkiye",
    "yapay zeka kısa film",
    "yapay zeka reklam filmi",
    "yapay zeka klip",
    "yapay zeka animasyon",
]

KEYWORDS_TOOLS = [
    "sora video",
    "runway video",
    "kling video",
    "seedance video",
    "minimax video",
    "pika video",
    "luma video",
    "veo video",
    "haiper video",
    "wan video",
]

HASHTAGS = [
    "#yapayzekavideosu", "#aiileyapıldı", "#aifilm", "#aianimasyon",
    "#aivideo", "#sora", "#runway", "#kling", "#minimax", "#pika",
    "#luma", "#veo", "#hailuo", "#haiper", "#wanvideo", "#seedance",
]

# Discovery Queries (Perplexity)
DISCOVERY_QUERIES = [
    "Türkiye'de bu hafta Seedance, Kling, Sora, Runway, Veo, Minimax, Pika, Luma ile YAPILMIŞ ve viral olan videoları listele. Video başlıkları, platform, kanal adı, kullanılan AI araç, izlenme sayısı ve linkleriyle JSON olarak ver.",
    "This week most viral AI-generated videos in Turkey made with Seedance Kling Sora Runway Veo Minimax. List title, platform, channel, AI tool used, view count and URL as JSON array.",
    "Türkiye'de yapay zeka ile üretilmiş reklam filmi veya müzik klibi son 1 hafta. Seedance, Kling, Veo, Sora, Runway kullanılmış olanlar. Marka, kanal, araç ve izlenme bilgileriyle listele.",
    "Turkish AI video creators Öner Biberkökü, stevedacinema, ujkatimbu, Nexor, 788 Studio latest viral videos this week. List with view counts, platforms, and AI tools used.",
]

SOCIAL_QUERIES = {
    "x": "X Twitter'da Türkiye'de son 3 günde en çok paylaşılan ve konuşulan yapay zeka videosu hangisi? Video linki, paylaşım sayısı, beğeni sayısı ile listele.",
    "tiktok": "TikTok'ta Türkiye'de son 3 günde en çok izlenen yapay zeka ile yapılmış videolar hangileri? İzlenme sayıları ve hesap adlarıyla listele.",
    "instagram": "Instagram Reels'te Türkiye'de son 3 günde viral olan yapay zeka videoları hangileri? İzlenme ve beğeni sayılarıyla listele.",
}

# VMW Score Weights
VMW_WEIGHTS = {
    "reach": {
        "max": 30,
        "view_count": 0.50,      # Toplam görüntülenme
        "velocity": 0.30,        # Erişim hızı
        "cross_platform": 0.20,  # Platform çeşitliliği
    },
    "engagement": {
        "max": 30,
        "rate": 0.40,            # Etkileşim oranı
        "comment_quality": 0.30, # Yorum kalitesi
        "share_save": 0.30,     # Paylaşım/kaydetme
    },
    "buzz": {
        "max": 25,
        "social_mention": 0.40,  # Sosyal medya bahsi
        "news_coverage": 0.30,   # Haber kapsamı
        "community": 0.30,      # Topluluk tartışması
    },
    "innovation": {
        "max": 15,
        "technical": 0.40,      # AI teknik karmaşıklık
        "creativity": 0.30,     # Yaratıcılık
        "quality": 0.30,        # Prodüksiyon kalitesi
    },
}

# View count thresholds for scoring (Reach)
VIEW_TIERS = [
    (10_000_000, 15),   # 10M+ → 15 puan
    (5_000_000, 13),
    (1_000_000, 11),
    (500_000, 9),
    (100_000, 7),
    (50_000, 5),
    (10_000, 3),
    (1_000, 1),
    (0, 0),
]

# AI Tools taxonomy
AI_TOOLS = {
    "video": ["Sora", "Runway", "Kling", "Seedance", "Minimax", "Pika", "Luma", "Veo", "Haiper", "Wan", "PixVerse"],
    "image": ["Midjourney", "DALL-E", "Stable Diffusion", "Flux", "Ideogram", "Imagen"],
    "audio": ["Suno", "Udio", "ElevenLabs"],
    "assist": ["ChatGPT", "Claude", "Gemini", "Topaz", "CapCut AI", "Magnific AI"],
}

"""
AI Video Market Watch — Perplexity Discovery Module

Perplexity API ile Türkiye'de viral AI videoları keşfeder.
Kullanım:
    from discovery import discover_ai_videos
    candidates = discover_ai_videos()
"""

import json
import re
import sys
from datetime import datetime

import requests

from config import (
    PERPLEXITY_API_KEY,
    PERPLEXITY_BASE_URL,
    PERPLEXITY_MODEL,
    PERPLEXITY_MAX_TOKENS,
    PERPLEXITY_TEMPERATURE,
    DISCOVERY_QUERIES,
    DATA_DIR,
)


def _call_perplexity(query, system_prompt=None):
    """Perplexity API'ye tek bir sorgu gönderir."""
    if not PERPLEXITY_API_KEY:
        print("[HATA] PERPLEXITY_API_KEY .env dosyasında tanımlı değil.")
        return None

    if system_prompt is None:
        system_prompt = (
            "Sen Türkiye'deki AI video pazarını takip eden bir analistsin. "
            "Sadece yapay zeka araçları (Seedance, Kling, Sora, Runway, Veo, Minimax, Pika, Luma, Midjourney vb.) "
            "kullanılarak ÜRETİLMİŞ videolar hakkında bilgi ver. AI hakkında haber/tartışma videoları değil, "
            "AI ile YAPILMIŞ içerikler. "
            "Yanıtını aşağıdaki JSON array formatında ver, başka açıklama ekleme:\n"
            '[{"title":"...","platform":"youtube/tiktok/instagram/x","channel":"...","ai_tools":["Seedance","Kling"],"estimated_views":150000,"url":"https://...","published_date":"2026-02-25"}]'
        )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": query},
    ]

    try:
        response = requests.post(
            PERPLEXITY_BASE_URL,
            headers={
                "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": PERPLEXITY_MODEL,
                "messages": messages,
                "max_tokens": PERPLEXITY_MAX_TOKENS,
                "temperature": PERPLEXITY_TEMPERATURE,
            },
            timeout=30,
        )
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]

    except requests.exceptions.RequestException as e:
        print(f"  [Perplexity HATA] {e}")
        return None


def _parse_video_candidates(raw_text):
    """
    Perplexity yanıtından video adaylarını parse eder.
    Hem JSON hem serbest metin formatını destekler.
    """
    candidates = []

    # Markdown code block içindeki JSON'ı temizle
    clean_text = raw_text.strip()
    if clean_text.startswith("```"):
        clean_text = re.sub(r'^```(?:json)?\s*', '', clean_text)
        clean_text = re.sub(r'\s*```\s*$', '', clean_text)

    # Önce tam JSON parse dene (obje veya array)
    try:
        parsed = json.loads(clean_text)
        items = _extract_video_list(parsed)
        for item in items:
            candidates.append(_normalize_candidate(item))
        if candidates:
            return candidates
    except (json.JSONDecodeError, ValueError):
        pass

    # JSON array bulmayı dene
    json_match = re.search(r'\[[\s\S]*?\]', raw_text)
    if json_match:
        try:
            parsed = json.loads(json_match.group())
            if isinstance(parsed, list):
                for item in parsed:
                    if isinstance(item, dict):
                        candidates.append(_normalize_candidate(item))
                if candidates:
                    return candidates
        except json.JSONDecodeError:
            pass

    # JSON obje içinde array bulmayı dene
    json_obj_match = re.search(r'\{[\s\S]*\}', raw_text)
    if json_obj_match:
        try:
            parsed = json.loads(json_obj_match.group())
            items = _extract_video_list(parsed)
            for item in items:
                candidates.append(_normalize_candidate(item))
            if candidates:
                return candidates
        except (json.JSONDecodeError, ValueError):
            pass

    # Serbest metin parse — her satır/paragraftan bilgi çıkar
    lines = raw_text.split("\n")
    current = {}

    for line in lines:
        line = line.strip()
        if not line:
            if current.get("title"):
                candidates.append(_normalize_candidate(current))
                current = {}
            continue

        # Başlık tespiti (numaralı liste veya bold)
        title_match = re.match(r'^[\d]+[\.\)]\s*\*?\*?(.+?)(?:\*?\*?\s*$)', line)
        if title_match:
            if current.get("title"):
                candidates.append(_normalize_candidate(current))
            current = {"title": title_match.group(1).strip()}
            continue

        # Platform tespiti
        for platform in ["YouTube", "TikTok", "Instagram", "X", "Twitter"]:
            if platform.lower() in line.lower():
                current["platform"] = "x" if platform.lower() in ["x", "twitter"] else platform.lower()

        # İzlenme tespiti
        view_match = re.search(r'(\d[\d.,]*)\s*(?:milyon|M)\s*(?:izlen|görüntülen|view)', line, re.IGNORECASE)
        if view_match:
            num = view_match.group(1).replace(".", "").replace(",", ".")
            current["estimated_views"] = int(float(num) * 1_000_000)

        view_match2 = re.search(r'(\d[\d.,]*)\s*(?:bin|K)\s*(?:izlen|görüntülen|view)', line, re.IGNORECASE)
        if view_match2:
            num = view_match2.group(1).replace(".", "").replace(",", ".")
            current["estimated_views"] = int(float(num) * 1_000)

        # Link tespiti
        url_match = re.search(r'(https?://[^\s\)]+)', line)
        if url_match:
            current["url"] = url_match.group(1)

        # AI araç tespiti
        for tool in ["Sora", "Runway", "Kling", "Seedance", "Minimax", "Pika", "Luma", "Veo", "Haiper", "Wan", "Midjourney", "DALL-E"]:
            if tool.lower() in line.lower():
                current.setdefault("ai_tools", []).append(tool)

        # Kanal/hesap tespiti
        account_match = re.search(r'@([\w.]+)', line)
        if account_match:
            current["channel"] = f"@{account_match.group(1)}"

    # Son entry
    if current.get("title"):
        candidates.append(_normalize_candidate(current))

    return candidates


def _extract_video_list(data):
    """JSON objesinden video listesini çıkart (iç içe yapıları destekler)."""
    if isinstance(data, list):
        return [item for item in data if isinstance(item, dict)]

    if isinstance(data, dict):
        # Direkt video alanları varsa (tek video)
        if any(k in data for k in ["title", "baslik", "başlık", "video_basligi"]):
            return [data]

        # İç içe array bul — herhangi bir key'in altında list varsa
        for key, value in data.items():
            if isinstance(value, list) and value:
                if isinstance(value[0], dict):
                    return value

        # Bir seviye daha in
        for key, value in data.items():
            if isinstance(value, dict):
                result = _extract_video_list(value)
                if result:
                    return result

    return []


def _parse_views(raw_value):
    """Çeşitli formatlardaki izlenme sayısını int'e çevir."""
    if isinstance(raw_value, (int, float)):
        return int(raw_value)
    if not isinstance(raw_value, str):
        return 0

    s = raw_value.strip().lower().replace(".", "").replace(",", ".")

    # "1.5M", "1.5 milyon" vb.
    m_match = re.search(r'([\d.]+)\s*(?:m|milyon)', s)
    if m_match:
        return int(float(m_match.group(1)) * 1_000_000)

    # "150K", "150 bin" vb.
    k_match = re.search(r'([\d.]+)\s*(?:k|bin)', s)
    if k_match:
        return int(float(k_match.group(1)) * 1_000)

    # Düz sayı
    num_match = re.search(r'([\d]+)', s)
    if num_match:
        return int(num_match.group(1))

    return 0


def _normalize_candidate(raw):
    """Video adayını standart formata dönüştürür (TR + EN field isimlerini destekler)."""

    # Başlık
    title = (
        raw.get("title")
        or raw.get("baslik")
        or raw.get("başlık")
        or raw.get("video_title")
        or raw.get("video_basligi")
        or "Bilinmiyor"
    )

    # Platform
    platform = (
        raw.get("platform")
        or raw.get("Platform")
        or "bilinmiyor"
    )

    # Kanal
    channel = (
        raw.get("channel")
        or raw.get("kanal")
        or raw.get("channel_name")
        or raw.get("kanal_hesap_adi")
        or raw.get("hesap")
        or raw.get("hesap_adi")
        or ""
    )

    # AI araçlar
    ai_tools = (
        raw.get("ai_tools")
        or raw.get("ai_tool")
        or raw.get("araç")
        or raw.get("kullanililan_ai_araci")
        or raw.get("kullanilan_ai_araci")
        or raw.get("ai_araci")
        or []
    )
    # String ise listeye çevir
    if isinstance(ai_tools, str):
        if ai_tools.lower() in ("belirtilmemiş", "bilinmiyor", "yok", ""):
            ai_tools = []
        else:
            ai_tools = [t.strip() for t in ai_tools.replace("/", ",").split(",") if t.strip()]

    # İzlenme
    views_raw = (
        raw.get("estimated_views")
        or raw.get("views")
        or raw.get("izlenme")
        or raw.get("tahmini_goruntulenme_sayisi")
        or raw.get("goruntulenme")
        or raw.get("view_count")
        or 0
    )
    estimated_views = _parse_views(views_raw)

    # URL
    url = (
        raw.get("url")
        or raw.get("link")
        or raw.get("video_url")
        or raw.get("video_linki")
        or ""
    )

    # Tarih
    pub_date = (
        raw.get("published_date")
        or raw.get("tarih")
        or raw.get("date")
        or raw.get("yayin_tarihi")
        or ""
    )

    return {
        "title": title,
        "platform": platform.lower() if isinstance(platform, str) else "bilinmiyor",
        "channel": channel,
        "ai_tools": ai_tools,
        "estimated_views": estimated_views,
        "url": url,
        "published_date": pub_date,
        "description": raw.get("description", raw.get("açıklama", "")),
        "metrics_source": "perplexity",
        "discovered_at": datetime.now().isoformat(),
    }


def discover_ai_videos(queries=None):
    """
    Perplexity ile AI video keşfi yapar.

    Returns:
        list[dict]: Video adayları listesi
    """
    if queries is None:
        queries = DISCOVERY_QUERIES

    all_candidates = []
    seen_titles = set()

    print(f"\n{'='*60}")
    print(f"Perplexity AI Video Keşfi — {len(queries)} sorgu")
    print(f"{'='*60}\n")

    for i, query in enumerate(queries, 1):
        print(f"  [{i}/{len(queries)}] Sorgu gönderiliyor...")
        raw = _call_perplexity(query)

        if raw:
            candidates = _parse_video_candidates(raw)
            new_count = 0
            for c in candidates:
                title_key = c["title"].lower().strip()
                if title_key not in seen_titles and title_key != "bilinmiyor":
                    seen_titles.add(title_key)
                    all_candidates.append(c)
                    new_count += 1
            print(f"         → {new_count} yeni video adayı")
        else:
            print(f"         → Yanıt alınamadı")

    print(f"\n[Keşif] Toplam {len(all_candidates)} benzersiz video adayı bulundu.")
    return all_candidates


def save_candidates(candidates, filename="discovery_latest.json"):
    """Adayları JSON olarak kaydet."""
    output_path = DATA_DIR / filename
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(candidates, f, ensure_ascii=False, indent=2, default=str)
    print(f"[Kayıt] {len(candidates)} aday → {output_path}")


# --- CLI ---
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Perplexity AI Video Discovery")
    parser.add_argument("--query", type=str, help="Özel arama sorgusu")

    args = parser.parse_args()

    if args.query:
        candidates = discover_ai_videos(queries=[args.query])
    else:
        candidates = discover_ai_videos()

    if candidates:
        print(f"\n{'='*60}")
        print(f"Bulunan Video Adayları:")
        print(f"{'='*60}")
        for i, c in enumerate(candidates, 1):
            tools_str = ", ".join(c["ai_tools"]) if isinstance(c["ai_tools"], list) else str(c["ai_tools"])
            print(f"\n  #{i} {c['title'][:70]}")
            print(f"     📺 {c['platform']} | 🎬 {c['channel']}")
            print(f"     🤖 AI: {tools_str or 'Bilinmiyor'}")
            if c.get("estimated_views"):
                print(f"     👁 ~{c['estimated_views']:,} (tahmini)")
            if c.get("url"):
                print(f"     🔗 {c['url']}")

        save_candidates(candidates)

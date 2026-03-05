"""
AI Video Market Watch — Report Generator

Günlük/haftalık raporları Markdown ve HTML olarak üretir.
Kullanım:
    from report_generator import generate_daily_report, generate_daily_report_html, generate_weekly_chart
"""

import html as html_mod
import json
import math
from collections import Counter
from datetime import datetime, timedelta
from pathlib import Path

from config import REPORTS_DIR, CHARTS_DIR, DATA_DIR
from scorer import vmw_level


def generate_daily_report(videos, date=None):
    """
    Günlük rapor üretir ve reports/daily/YYYY-MM-DD.md olarak kaydeder.

    Args:
        videos: list[dict] — skorlanmış video listesi
        date: str — rapor tarihi (default: bugün)

    Returns:
        Path: oluşturulan dosya yolu
    """
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")

    weekday_tr = {0: "Pazartesi", 1: "Salı", 2: "Çarşamba", 3: "Perşembe",
                  4: "Cuma", 5: "Cumartesi", 6: "Pazar"}
    dt = datetime.strptime(date, "%Y-%m-%d")
    day_name = weekday_tr.get(dt.weekday(), "")

    # YouTube vs tahmini ayır
    yt_videos = [v for v in videos if v.get("metrics_source") == "api"]
    est_videos = [v for v in videos if v.get("metrics_source") != "api"]

    lines = [
        f"# AI Video Market Watch - Günlük Rapor",
        f"**Tarih:** {date} ({day_name})",
        f"**Toplam Tespit:** {len(videos)} video",
        f"**Kesin Metrik:** {len(yt_videos)} (YouTube API) | **Tahmini:** {len(est_videos)} (Perplexity)",
        "",
        "---",
        "",
        "## Top 10 (VMW Score)",
        "",
        "| # | Video | Platform | Kanal | AI Araç | İzlenme | VMW | Seviye |",
        "|---|-------|----------|-------|---------|---------|-----|--------|",
    ]

    for i, v in enumerate(videos[:10], 1):
        title = v.get("title", "Bilinmiyor")[:50]
        platform = v.get("platform", "?")
        channel = v.get("channel_title", v.get("channel", "?"))[:20]
        tools = v.get("ai_tools", [])
        tools_str = ", ".join(tools) if isinstance(tools, list) else str(tools) if tools else "?"
        views = v.get("view_count", v.get("estimated_views", 0))
        source_mark = "" if v.get("metrics_source") == "api" else "~"
        vmw = v.get("vmw_score", 0)
        level = vmw_level(vmw)

        if views >= 1_000_000:
            views_str = f"{source_mark}{views/1_000_000:.1f}M"
        elif views >= 1_000:
            views_str = f"{source_mark}{views/1_000:.0f}K"
        else:
            views_str = f"{source_mark}{views:,}"

        lines.append(f"| {i} | {title} | {platform} | {channel} | {tools_str} | {views_str} | **{vmw}** | {level} |")

    lines.extend([
        "",
        "---",
        "",
        "## Tüm Videolar (Detaylı)",
        "",
    ])

    for i, v in enumerate(videos, 1):
        title = v.get("title", "Bilinmiyor")
        vmw = v.get("vmw_score", 0)
        views = v.get("view_count", v.get("estimated_views", 0))
        likes = v.get("like_count", 0)
        comments = v.get("comment_count", 0)
        platform = v.get("platform", "?")
        channel = v.get("channel_title", v.get("channel", "?"))
        tools = v.get("ai_tools", [])
        tools_str = ", ".join(tools) if isinstance(tools, list) else str(tools) if tools else "Bilinmiyor"
        url = v.get("url", "")
        source = "Doğrulanmış" if v.get("metrics_source") == "api" else "Tahmini"

        lines.extend([
            f"### #{i} — {title}",
            f"- **VMW Score:** {vmw}/100 ({vmw_level(vmw)})",
            f"- **Platform:** {platform}",
            f"- **Kanal/Hesap:** {channel}",
            f"- **AI Araç:** {tools_str}",
            f"- **İzlenme:** {views:,} ({source})",
            f"- **Beğeni:** {likes:,} | **Yorum:** {comments:,}",
        ])
        if url:
            lines.append(f"- **Link:** {url}")

        # VMW Breakdown
        breakdown = v.get("vmw_breakdown", {})
        if breakdown:
            lines.extend([
                f"- **Skor Detay:** R:{v.get('vmw_reach', 0)}/30 | E:{v.get('vmw_engagement', 0)}/30 | B:{v.get('vmw_buzz', 0)}/25 | I:{v.get('vmw_innovation', 0)}/15",
            ])
        lines.append("")

    # Metrik kaynağı notu
    lines.extend([
        "---",
        "",
        "## Veri Kaynağı",
        f"- YouTube API: {len(yt_videos)} video (kesin metrik)",
        f"- Perplexity: {len(est_videos)} video (tahmini metrik, ~ ile işaretli)",
        f"- Rapor oluşturma: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "---",
        "",
        f"*VMW Agent — Günlük Rapor*",
        f"*{date}*",
    ])

    # Kaydet
    output_dir = REPORTS_DIR / "daily"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{date}.md"

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"[Rapor] Günlük rapor → {output_path}")
    return output_path


def _esc(text):
    """HTML-escape helper."""
    return html_mod.escape(str(text)) if text else ""


def _fmt_views(views):
    """Format view count: 7.9M, 79K, 1,234."""
    if views >= 1_000_000:
        return f"{views / 1_000_000:.1f}M"
    elif views >= 1_000:
        return f"{views / 1_000:.0f}K"
    return f"{views:,}"


def _score_class(vmw):
    """Return CSS class for a VMW score."""
    if vmw >= 40:
        return "high"
    elif vmw >= 30:
        return "mid"
    return "low"


def _level_class(vmw):
    """Return CSS class for level badge."""
    if vmw >= 40:
        return "iyi"
    elif vmw >= 30:
        return "ortalama"
    return "dusuk"


def _rank_class(i):
    """Return rank medal CSS class."""
    if i == 1:
        return " gold"
    elif i == 2:
        return " silver"
    elif i == 3:
        return " bronze"
    return ""


def generate_daily_report_html(videos, date=None):
    """
    Günlük Apple-style HTML rapor üretir ve reports/daily/YYYY-MM-DD.html olarak kaydeder.

    Args:
        videos: list[dict] — skorlanmış video listesi
        date: str — rapor tarihi (default: bugün)

    Returns:
        Path: oluşturulan dosya yolu
    """
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")

    weekday_tr = {0: "Pazartesi", 1: "Sali", 2: "Carsamba", 3: "Persembe",
                  4: "Cuma", 5: "Cumartesi", 6: "Pazar"}
    month_tr = {1: "Ocak", 2: "Subat", 3: "Mart", 4: "Nisan", 5: "Mayis", 6: "Haziran",
                7: "Temmuz", 8: "Agustos", 9: "Eylul", 10: "Ekim", 11: "Kasim", 12: "Aralik"}
    dt = datetime.strptime(date, "%Y-%m-%d")
    day_name = weekday_tr.get(dt.weekday(), "")
    date_display = f"{dt.day} {month_tr.get(dt.month, '')} {dt.year}, {day_name}"

    # --- Stats ---
    total = len(videos)
    max_vmw = max((v.get("vmw_score", 0) for v in videos), default=0)
    max_views = max((v.get("view_count", v.get("estimated_views", 0)) for v in videos), default=0)
    yt_count = sum(1 for v in videos if v.get("metrics_source") == "api")
    est_count = total - yt_count

    # Unique AI tools across all videos
    all_tools = set()
    for v in videos:
        tools = v.get("ai_tools", [])
        if isinstance(tools, list):
            all_tools.update(tools)
    unique_tools = len(all_tools)

    # --- Score distribution ---
    iyi_count = sum(1 for v in videos if v.get("vmw_score", 0) >= 40)
    ortalama_count = sum(1 for v in videos if 30 <= v.get("vmw_score", 0) < 40)
    dusuk_count = sum(1 for v in videos if v.get("vmw_score", 0) < 30)

    # Donut chart math (circumference = 2 * pi * 80 ≈ 502.65)
    circ = 2 * math.pi * 80
    iyi_arc = (iyi_count / total * circ) if total else 0
    ortalama_arc = (ortalama_count / total * circ) if total else 0
    dusuk_arc = (dusuk_count / total * circ) if total else 0

    # --- AI tool counts (all videos) ---
    tool_counter = Counter()
    for v in videos:
        tools = v.get("ai_tools", [])
        if isinstance(tools, list):
            for t in tools:
                if t:
                    tool_counter[t] += 1
    top_tools = tool_counter.most_common(10)

    # --- Build tool cards HTML ---
    tool_cards_html = ""
    for tool_name, count in top_tools:
        tool_cards_html += f"""
        <div class="tool-card">
            <div class="tool-count">{count}</div>
            <div class="tool-name">{_esc(tool_name)}</div>
            <div class="tool-count-label">video</div>
        </div>"""

    # --- Build Top 10 cards HTML ---
    top10 = videos[:10]
    top10_cards_html = ""
    for i, v in enumerate(top10, 1):
        title = _esc(v.get("title", "Bilinmiyor"))[:80]
        channel = _esc(v.get("channel_title", v.get("channel", "?")))[:30]
        url = v.get("url", "#")
        vmw = v.get("vmw_score", 0)
        views = v.get("view_count", v.get("estimated_views", 0))
        tools = v.get("ai_tools", [])
        if not isinstance(tools, list):
            tools = [str(tools)] if tools else []

        tool_badges = "".join(f'<span class="tool-badge">{_esc(t)}</span>' for t in tools if t)

        top10_cards_html += f"""
    <div class="top-video-card">
        <div class="rank{_rank_class(i)}">{i}</div>
        <div class="video-info">
            <div class="video-title"><a href="{_esc(url)}" target="_blank">{title}</a></div>
            <div class="video-meta">
                <span class="meta-tag"><span class="icon">&#x1F4FA;</span> {_esc(channel)}</span>
                {tool_badges}
            </div>
        </div>
        <div class="video-stats">
            <div class="vmw-score">
                <div class="score-bar-bg"><div class="score-bar-fill {_score_class(vmw)}" style="width:{vmw}%"></div></div>
                <span class="score-number {_score_class(vmw)}">{vmw}</span>
            </div>
            <span class="views-count">{_fmt_views(views)} izlenme</span>
        </div>
    </div>"""

    # --- Build score breakdown table rows ---
    score_rows_html = ""
    for i, v in enumerate(top10, 1):
        title = _esc(v.get("title", "?"))[:45]
        url = v.get("url", "#")
        vmw = v.get("vmw_score", 0)
        r = v.get("vmw_reach", 0)
        e = v.get("vmw_engagement", 0)
        b = v.get("vmw_buzz", 0)
        inn = v.get("vmw_innovation", 0)
        level = vmw_level(vmw)
        lc = _level_class(vmw)

        score_rows_html += f"""
                <tr>
                    <td>{i}</td>
                    <td class="title-cell"><a href="{_esc(url)}" target="_blank">{title}</a></td>
                    <td><strong>{vmw}</strong></td>
                    <td><span class="mini-bar" style="width:{r * 2.5}px;background:#5ac8fa"></span>{r}</td>
                    <td><span class="mini-bar" style="width:{e * 2.5}px;background:#af52de"></span>{e}</td>
                    <td><span class="mini-bar" style="width:{b * 2.5}px;background:#ff9500"></span>{b}</td>
                    <td><span class="mini-bar" style="width:{inn * 2.5}px;background:#34c759"></span>{inn}</td>
                    <td><span class="level-badge {lc}">{level}</span></td>
                </tr>"""

    # --- Assemble full HTML ---
    html_content = f"""<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Video Market Watch &mdash; {date_display}</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        :root {{
            --text-primary: #1d1d1f; --text-secondary: #6e6e73; --text-tertiary: #86868b;
            --bg-primary: #ffffff; --bg-secondary: #f5f5f7;
            --border-light: #e8e8ed;
            --accent-blue: #0071e3; --accent-green: #34c759; --accent-orange: #ff9500;
            --accent-red: #ff3b30; --accent-purple: #af52de; --accent-teal: #5ac8fa;
            --shadow-sm: 0 1px 3px rgba(0,0,0,0.04); --shadow-md: 0 4px 16px rgba(0,0,0,0.06);
            --radius-sm: 12px; --radius-md: 16px;
        }}
        body {{ font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'SF Pro Display', sans-serif; background: var(--bg-primary); color: var(--text-primary); -webkit-font-smoothing: antialiased; line-height: 1.5; }}
        .hero {{ padding: 80px 0 40px; text-align: center; background: linear-gradient(180deg, #f5f5f7 0%, #fff 100%); }}
        .hero-badge {{ display: inline-flex; align-items: center; gap: 6px; padding: 6px 14px; background: var(--bg-primary); border: 1px solid var(--border-light); border-radius: 100px; font-size: 13px; font-weight: 500; color: var(--text-secondary); margin-bottom: 20px; box-shadow: var(--shadow-sm); }}
        .hero-badge .dot {{ width: 8px; height: 8px; border-radius: 50%; background: var(--accent-green); animation: pulse 2s infinite; }}
        @keyframes pulse {{ 0%, 100% {{ opacity: 1; }} 50% {{ opacity: 0.5; }} }}
        .hero h1 {{ font-size: 48px; font-weight: 700; letter-spacing: -0.03em; margin-bottom: 8px; }}
        .hero .subtitle {{ font-size: 22px; color: var(--text-secondary); }}
        .hero .date {{ font-size: 17px; color: var(--text-tertiary); margin-top: 12px; }}
        .container {{ max-width: 1120px; margin: 0 auto; padding: 0 24px; }}
        .stats-row {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; padding: 40px 0; }}
        .stat-card {{ background: var(--bg-secondary); border-radius: var(--radius-md); padding: 24px; text-align: center; transition: transform 0.2s ease; }}
        .stat-card:hover {{ transform: translateY(-2px); }}
        .stat-value {{ font-size: 36px; font-weight: 700; letter-spacing: -0.02em; }}
        .stat-value.blue {{ color: var(--accent-blue); }} .stat-value.green {{ color: var(--accent-green); }}
        .stat-value.orange {{ color: var(--accent-orange); }} .stat-value.purple {{ color: var(--accent-purple); }}
        .stat-label {{ font-size: 14px; font-weight: 500; color: var(--text-secondary); margin-top: 4px; }}
        .section {{ padding: 48px 0; }}
        .section-header {{ margin-bottom: 32px; }}
        .section-title {{ font-size: 32px; font-weight: 700; letter-spacing: -0.02em; }}
        .section-subtitle {{ font-size: 17px; color: var(--text-secondary); margin-top: 8px; }}
        .divider {{ height: 1px; background: var(--border-light); }}
        .top-video-card {{ display: grid; grid-template-columns: 56px 1fr auto; align-items: center; gap: 20px; padding: 20px 0; border-bottom: 1px solid var(--border-light); transition: background 0.15s ease; }}
        .top-video-card:last-child {{ border-bottom: none; }}
        .top-video-card:hover {{ background: var(--bg-secondary); margin: 0 -16px; padding: 20px 16px; border-radius: var(--radius-sm); }}
        .rank {{ width: 56px; height: 56px; display: flex; align-items: center; justify-content: center; font-size: 22px; font-weight: 700; background: var(--bg-secondary); border-radius: var(--radius-sm); flex-shrink: 0; }}
        .rank.gold {{ background: linear-gradient(135deg, #ffd60a20, #ffd60a10); color: #b8860b; }}
        .rank.silver {{ background: linear-gradient(135deg, #8e8e9320, #8e8e9310); color: #6e6e73; }}
        .rank.bronze {{ background: linear-gradient(135deg, #cd7f3220, #cd7f3210); color: #cd7f32; }}
        .video-info {{ min-width: 0; }}
        .video-title {{ font-size: 16px; font-weight: 600; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; margin-bottom: 4px; }}
        .video-title a {{ color: inherit; text-decoration: none; }} .video-title a:hover {{ color: var(--accent-blue); }}
        .video-meta {{ display: flex; align-items: center; gap: 12px; flex-wrap: wrap; }}
        .meta-tag {{ display: inline-flex; align-items: center; gap: 4px; font-size: 13px; color: var(--text-secondary); }}
        .tool-badge {{ display: inline-flex; padding: 2px 10px; background: var(--bg-secondary); border-radius: 100px; font-size: 12px; font-weight: 500; color: var(--accent-blue); border: 1px solid rgba(0,113,227,0.1); }}
        .video-stats {{ display: flex; flex-direction: column; align-items: flex-end; gap: 6px; flex-shrink: 0; }}
        .vmw-score {{ display: flex; align-items: center; gap: 8px; }}
        .score-bar-bg {{ width: 80px; height: 6px; background: var(--border-light); border-radius: 3px; overflow: hidden; }}
        .score-bar-fill {{ height: 100%; border-radius: 3px; }}
        .score-bar-fill.high {{ background: var(--accent-green); }} .score-bar-fill.mid {{ background: var(--accent-orange); }} .score-bar-fill.low {{ background: var(--accent-red); }}
        .score-number {{ font-size: 20px; font-weight: 700; min-width: 36px; text-align: right; }}
        .score-number.high {{ color: var(--accent-green); }} .score-number.mid {{ color: var(--accent-orange); }} .score-number.low {{ color: var(--accent-red); }}
        .views-count {{ font-size: 13px; color: var(--text-tertiary); font-weight: 500; }}
        .tools-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 12px; }}
        .tool-card {{ background: var(--bg-secondary); border-radius: var(--radius-sm); padding: 20px; text-align: center; transition: transform 0.2s ease, box-shadow 0.2s ease; }}
        .tool-card:hover {{ transform: translateY(-2px); box-shadow: var(--shadow-md); }}
        .tool-name {{ font-size: 15px; font-weight: 600; margin-bottom: 4px; }}
        .tool-count {{ font-size: 28px; font-weight: 700; color: var(--accent-blue); }}
        .tool-count-label {{ font-size: 12px; color: var(--text-tertiary); font-weight: 500; }}
        .score-table-wrapper {{ overflow-x: auto; border-radius: var(--radius-md); border: 1px solid var(--border-light); }}
        .score-table {{ width: 100%; border-collapse: collapse; font-size: 14px; }}
        .score-table thead {{ background: var(--bg-secondary); }}
        .score-table th {{ padding: 14px 16px; text-align: left; font-weight: 600; color: var(--text-secondary); font-size: 12px; text-transform: uppercase; letter-spacing: 0.05em; white-space: nowrap; }}
        .score-table td {{ padding: 14px 16px; border-top: 1px solid var(--border-light); white-space: nowrap; }}
        .score-table tbody tr:hover {{ background: rgba(0,113,227,0.02); }}
        .score-table .title-cell {{ max-width: 280px; overflow: hidden; text-overflow: ellipsis; font-weight: 500; }}
        .score-table .title-cell a {{ color: var(--text-primary); text-decoration: none; }} .score-table .title-cell a:hover {{ color: var(--accent-blue); }}
        .mini-bar {{ display: inline-block; height: 4px; border-radius: 2px; margin-right: 6px; vertical-align: middle; }}
        .level-badge {{ display: inline-flex; padding: 3px 10px; border-radius: 100px; font-size: 12px; font-weight: 600; }}
        .level-badge.iyi {{ background: #34c75915; color: #248a3d; }}
        .level-badge.ortalama {{ background: #ff950015; color: #c93400; }}
        .level-badge.dusuk {{ background: #ff3b3015; color: #d70015; }}
        .score-donut-section {{ display: grid; grid-template-columns: 1fr 1fr; gap: 32px; align-items: center; }}
        .score-legend {{ display: flex; flex-direction: column; gap: 16px; }}
        .legend-item {{ display: flex; align-items: center; gap: 12px; }}
        .legend-dot {{ width: 12px; height: 12px; border-radius: 50%; flex-shrink: 0; }}
        .legend-label {{ font-size: 15px; color: var(--text-secondary); flex: 1; }}
        .legend-value {{ font-size: 15px; font-weight: 600; }}
        .insight-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 16px; }}
        .insight-card {{ background: var(--bg-secondary); border-radius: var(--radius-md); padding: 24px; }}
        .insight-card h3 {{ font-size: 17px; font-weight: 600; margin-bottom: 8px; }}
        .insight-card p {{ font-size: 14px; color: var(--text-secondary); line-height: 1.6; }}
        .footer {{ padding: 48px 0; text-align: center; border-top: 1px solid var(--border-light); margin-top: 48px; }}
        .footer p {{ font-size: 13px; color: var(--text-tertiary); }}
        .footer .logo {{ font-size: 18px; font-weight: 700; color: var(--text-primary); margin-bottom: 8px; letter-spacing: -0.02em; }}
        @media (max-width: 768px) {{
            .hero h1 {{ font-size: 32px; }} .hero .subtitle {{ font-size: 18px; }}
            .stats-row {{ grid-template-columns: repeat(2, 1fr); }}
            .top-video-card {{ grid-template-columns: 44px 1fr; gap: 12px; }}
            .video-stats {{ display: none; }}
            .rank {{ width: 44px; height: 44px; font-size: 18px; }}
            .score-donut-section {{ grid-template-columns: 1fr; }}
            .section-title {{ font-size: 24px; }}
        }}
        @media print {{
            .hero {{ padding: 40px 0 20px; }}
            .stat-card:hover, .tool-card:hover, .top-video-card:hover {{ transform: none; }}
        }}
    </style>
</head>
<body>

<!-- Logo -->
<div style="text-align:center; padding: 48px 0 0;">
    <img src="Untitled 2.jpg" alt="AI Yapim" style="height: 64px; width: auto;">
</div>

<!-- Hero -->
<header class="hero" style="padding-top: 24px;">
    <div class="container">
        <div class="hero-badge">
            <span class="dot"></span>
            YouTube API &mdash; Dogrulanmis Veri
        </div>
        <h1>AI Video Market Watch</h1>
        <p class="subtitle">Gunluk Pazar Raporu</p>
        <p class="date">{date_display}</p>
    </div>
</header>

<!-- Stats -->
<section class="container">
    <div class="stats-row">
        <div class="stat-card">
            <div class="stat-value blue">{total}</div>
            <div class="stat-label">Toplam Video</div>
        </div>
        <div class="stat-card">
            <div class="stat-value green">{max_vmw}</div>
            <div class="stat-label">En Yuksek VMW</div>
        </div>
        <div class="stat-card">
            <div class="stat-value orange">{_fmt_views(max_views)}</div>
            <div class="stat-label">En Yuksek Izlenme</div>
        </div>
        <div class="stat-card">
            <div class="stat-value purple">{unique_tools}+</div>
            <div class="stat-label">AI Arac</div>
        </div>
    </div>
</section>

<div class="container"><div class="divider"></div></div>

<!-- Score Distribution -->
<section class="container section">
    <div class="section-header">
        <h2 class="section-title">Skor Dagilimi</h2>
        <p class="section-subtitle">{total} videonun VMW Score dagilimi</p>
    </div>
    <div class="score-donut-section">
        <div>
            <svg viewBox="0 0 200 200" width="220" height="220" style="display:block;margin:0 auto">
                <circle cx="100" cy="100" r="80" fill="none" stroke="#e8e8ed" stroke-width="24"/>
                <circle cx="100" cy="100" r="80" fill="none" stroke="#34c759" stroke-width="24"
                    stroke-dasharray="{iyi_arc:.1f} {circ - iyi_arc:.1f}" stroke-dashoffset="0"
                    transform="rotate(-90 100 100)" stroke-linecap="round"/>
                <circle cx="100" cy="100" r="80" fill="none" stroke="#ff9500" stroke-width="24"
                    stroke-dasharray="{ortalama_arc:.1f} {circ - ortalama_arc:.1f}" stroke-dashoffset="-{iyi_arc:.1f}"
                    transform="rotate(-90 100 100)" stroke-linecap="round"/>
                <circle cx="100" cy="100" r="80" fill="none" stroke="#ff3b30" stroke-width="24"
                    stroke-dasharray="{dusuk_arc:.1f} {circ - dusuk_arc:.1f}" stroke-dashoffset="-{iyi_arc + ortalama_arc:.1f}"
                    transform="rotate(-90 100 100)" stroke-linecap="round"/>
                <text x="100" y="92" text-anchor="middle" font-size="28" font-weight="700" fill="#1d1d1f" font-family="Inter, sans-serif">{total}</text>
                <text x="100" y="114" text-anchor="middle" font-size="13" fill="#86868b" font-family="Inter, sans-serif">video</text>
            </svg>
        </div>
        <div class="score-legend">
            <div class="legend-item">
                <div class="legend-dot" style="background:#34c759"></div>
                <span class="legend-label">Iyi (40+)</span>
                <span class="legend-value">{iyi_count} video</span>
            </div>
            <div class="legend-item">
                <div class="legend-dot" style="background:#ff9500"></div>
                <span class="legend-label">Ortalama (30-39)</span>
                <span class="legend-value">{ortalama_count} video</span>
            </div>
            <div class="legend-item">
                <div class="legend-dot" style="background:#ff3b30"></div>
                <span class="legend-label">Dusuk (0-29)</span>
                <span class="legend-value">{dusuk_count} video</span>
            </div>
        </div>
    </div>
</section>

<div class="container"><div class="divider"></div></div>

<!-- AI Tools -->
<section class="container section">
    <div class="section-header">
        <h2 class="section-title">AI Arac Kullanimi</h2>
        <p class="section-subtitle">Icerik uretiminde kullanilan AI araclari</p>
    </div>
    <div class="tools-grid">{tool_cards_html}
    </div>
</section>

<div class="container"><div class="divider"></div></div>

<!-- Top 10 -->
<section class="container section">
    <div class="section-header">
        <h2 class="section-title">Top 10</h2>
        <p class="section-subtitle">En yuksek VMW Score'a sahip videolar</p>
    </div>
    {top10_cards_html}
</section>

<div class="container"><div class="divider"></div></div>

<!-- Score Breakdown Table -->
<section class="container section">
    <div class="section-header">
        <h2 class="section-title">Detayli Skor Tablosu</h2>
        <p class="section-subtitle">Top 10 video icin R (Reach), E (Engagement), B (Buzz), I (Innovation) skor detaylari</p>
    </div>
    <div class="score-table-wrapper">
        <table class="score-table">
            <thead>
                <tr><th>#</th><th>Video</th><th>VMW</th><th>R /30</th><th>E /30</th><th>B /25</th><th>I /15</th><th>Seviye</th></tr>
            </thead>
            <tbody>{score_rows_html}
            </tbody>
        </table>
    </div>
    <div style="margin-top: 20px; display: flex; gap: 24px; flex-wrap: wrap;">
        <div style="display:flex;align-items:center;gap:6px;font-size:13px;color:var(--text-tertiary);"><span class="mini-bar" style="width:12px;background:#5ac8fa;display:inline-block"></span> R &mdash; Reach</div>
        <div style="display:flex;align-items:center;gap:6px;font-size:13px;color:var(--text-tertiary);"><span class="mini-bar" style="width:12px;background:#af52de;display:inline-block"></span> E &mdash; Engagement</div>
        <div style="display:flex;align-items:center;gap:6px;font-size:13px;color:var(--text-tertiary);"><span class="mini-bar" style="width:12px;background:#ff9500;display:inline-block"></span> B &mdash; Buzz</div>
        <div style="display:flex;align-items:center;gap:6px;font-size:13px;color:var(--text-tertiary);"><span class="mini-bar" style="width:12px;background:#34c759;display:inline-block"></span> I &mdash; Innovation</div>
    </div>
</section>

<!-- Footer -->
<footer class="footer">
    <div class="container">
        <p class="logo">VMW Agent</p>
        <p>AI Video Market Watch &mdash; Gunluk Rapor</p>
        <p style="margin-top:4px;">{date_display} &bull; Rapor olusturma: {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
        <p style="margin-top:16px; font-size:12px; color: #c7c7cc;">Veri Kaynagi: YouTube API ({yt_count} video, kesin metrik){f" | Perplexity ({est_count} video, tahmini)" if est_count else ""}</p>
    </div>
</footer>

</body>
</html>"""

    # Kaydet
    output_dir = REPORTS_DIR / "daily"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{date}.html"

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"[Rapor] Günlük HTML rapor → {output_path}")
    return output_path


def generate_weekly_chart_html(videos, week_label=None):
    """
    Haftalık Top 10 HTML chart üretir.

    Args:
        videos: list[dict] — skorlanmış ve sıralanmış top 10
        week_label: str — hafta etiketi (örn: "2026-W09")

    Returns:
        Path: oluşturulan HTML dosya yolu
    """
    if week_label is None:
        now = datetime.now()
        week_label = f"{now.year}-W{now.isocalendar()[1]:02d}"

    top10 = videos[:10]

    rows_html = ""
    for i, v in enumerate(top10, 1):
        title = v.get("title", "Bilinmiyor")[:60]
        platform = v.get("platform", "?").upper()
        channel = v.get("channel_title", v.get("channel", "?"))[:25]
        vmw = v.get("vmw_score", 0)
        views = v.get("view_count", v.get("estimated_views", 0))
        url = v.get("url", "#")
        tools = v.get("ai_tools", [])
        tools_str = ", ".join(tools) if isinstance(tools, list) else str(tools) if tools else "?"
        level = vmw_level(vmw)

        if views >= 1_000_000:
            views_str = f"{views/1_000_000:.1f}M"
        elif views >= 1_000:
            views_str = f"{views/1_000:.0f}K"
        else:
            views_str = f"{views:,}"

        bar_width = vmw  # 0-100 direkt yüzde olarak kullan

        medal = ""
        if i == 1: medal = "🥇"
        elif i == 2: medal = "🥈"
        elif i == 3: medal = "🥉"

        rows_html += f"""
        <tr>
            <td class="rank">{medal} #{i}</td>
            <td class="title"><a href="{url}" target="_blank">{title}</a></td>
            <td class="platform">{platform}</td>
            <td class="channel">{channel}</td>
            <td class="tools">{tools_str}</td>
            <td class="views">{views_str}</td>
            <td class="score">
                <div class="score-bar">
                    <div class="score-fill" style="width: {bar_width}%">{vmw}</div>
                </div>
                <span class="level">{level}</span>
            </td>
        </tr>"""

    html = f"""<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Video Market Watch — Top 10 | {week_label}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #0a0a0a; color: #e0e0e0; padding: 40px 20px; }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        h1 {{ font-size: 28px; font-weight: 700; color: #fff; margin-bottom: 8px; }}
        .subtitle {{ color: #888; font-size: 14px; margin-bottom: 32px; }}
        table {{ width: 100%; border-collapse: collapse; }}
        th {{ text-align: left; padding: 12px 16px; color: #888; font-size: 12px; text-transform: uppercase; letter-spacing: 0.5px; border-bottom: 1px solid #222; }}
        td {{ padding: 14px 16px; border-bottom: 1px solid #1a1a1a; font-size: 14px; }}
        tr:hover {{ background: #111; }}
        .rank {{ width: 60px; font-weight: 700; font-size: 16px; }}
        .title a {{ color: #58a6ff; text-decoration: none; }}
        .title a:hover {{ text-decoration: underline; }}
        .platform {{ color: #888; font-size: 12px; text-transform: uppercase; }}
        .channel {{ color: #aaa; }}
        .tools {{ color: #7ee787; font-size: 12px; }}
        .views {{ font-weight: 600; color: #f0f0f0; }}
        .score {{ width: 180px; }}
        .score-bar {{ background: #1a1a1a; border-radius: 4px; height: 24px; overflow: hidden; position: relative; }}
        .score-fill {{ height: 100%; background: linear-gradient(90deg, #238636, #58a6ff); border-radius: 4px; display: flex; align-items: center; justify-content: center; font-size: 12px; font-weight: 700; color: #fff; min-width: 30px; }}
        .level {{ display: block; font-size: 11px; color: #888; margin-top: 4px; text-align: center; }}
        .footer {{ margin-top: 40px; padding-top: 20px; border-top: 1px solid #222; color: #555; font-size: 12px; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>AI Video Market Watch — Top 10</h1>
        <p class="subtitle">Hafta: {week_label} | Türkiye AI Video Chart</p>

        <table>
            <thead>
                <tr>
                    <th>Sıra</th>
                    <th>Video</th>
                    <th>Platform</th>
                    <th>Kanal</th>
                    <th>AI Araç</th>
                    <th>İzlenme</th>
                    <th>VMW Score</th>
                </tr>
            </thead>
            <tbody>
                {rows_html}
            </tbody>
        </table>

        <div class="footer">
            <p>AI Video Market Watch — VMW Score: Reach (30) + Engagement (30) + Buzz (25) + Innovation (15) = 100</p>
            <p>Oluşturulma: {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
        </div>
    </div>
</body>
</html>"""

    output_dir = CHARTS_DIR / "weekly"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{week_label}.html"

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"[Chart] HTML Top 10 → {output_path}")
    return output_path


# --- CLI ---
if __name__ == "__main__":
    # Test data ile örnek rapor
    test_videos = [
        {
            "title": "Test Video 1",
            "platform": "youtube",
            "channel_title": "TestKanal",
            "ai_tools": ["Seedance"],
            "view_count": 1_500_000,
            "like_count": 45_000,
            "comment_count": 1_200,
            "vmw_score": 78,
            "vmw_reach": 22,
            "vmw_engagement": 24,
            "vmw_buzz": 20,
            "vmw_innovation": 12,
            "metrics_source": "api",
            "url": "https://youtube.com/watch?v=test",
        },
    ]
    print("[Test] Rapor üretiliyor...")
    generate_daily_report(test_videos, date="2026-01-01")
    generate_weekly_chart_html(test_videos, week_label="2026-W01")
    print("[Test] Tamamlandı.")

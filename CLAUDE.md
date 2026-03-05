# AI Video Market Watch - Türkiye

## Proje Tanımı

Türkiye'de popüler olan AI ile yapılmış videoların **günlük takibi, skorlanması, Top 10 chart oluşturması ve insight raporlaması** için oluşturulmuş market watch sistemi.

**Hedef:** Türkiye'deki AI video ekosistemini sistematik olarak izlemek, en başarılı içerikleri tespit etmek ve başarı faktörlerini analiz etmek.

---

## Kapsam

### İzlenen Platformlar
| Platform | Format | Metrikler |
|----------|--------|-----------|
| YouTube | Uzun video (1dk+) | Görüntülenme, beğeni, yorum, paylaşım |
| YouTube Shorts | Kısa video (<60sn) | Görüntülenme, beğeni, yorum |
| Instagram Reels | Kısa video | Görüntülenme, beğeni, yorum, kaydetme, paylaşım |
| TikTok | Kısa/orta video | Görüntülenme, beğeni, yorum, paylaşım, kaydetme |
| X (Twitter) | Video post | Görüntülenme, retweet, beğeni, alıntı, yer imi |

### AI Video Tespit Yöntemi: Hibrit

**1. Keyword/Hashtag Taraması:**
- Türkçe: `#yapayzekavideosu`, `#aiileyapıldı`, `#aifilm`, `#yapayzekafilm`, `#aianimasyon`, `#aisanat`
- İngilizce (Türkiye kaynaklı): `#aivideo`, `#sora`, `#runway`, `#kling`, `#minimax`, `#pika`, `#luma`, `#haiper`, `#veo`, `#midjourney`
- Başlık/açıklama keyword'leri: "yapay zeka ile", "AI ile yaptım", "sora ile", "runway ile", "kling ile" vb.

**2. Bilinen Kanal/Hesap Takibi:**
- Aktif AI video üreticileri Türkiye listesi (büyüyen liste, `data/tracked_channels.md` dosyasında tutulur)
- AI araç şirketlerinin Türkiye showcase hesapları
- Popüler tech/AI YouTube kanalları

**3. Topluluk Keşfi:**
- Reddit r/turkishAI, Ekşi Sözlük, Technopat gibi forumlarda viral AI video paylaşımları
- Haber sitelerinde (Webtekno, Shiftdelete, Donanımhaber) AI video haberleri

---

## Veri Toplama Mimarisi

### Aktif: YouTube Data API v3
- **Ana veri kaynağı** — keyword araması + video metrikleri
- Kesin metrikler: görüntülenme, beğeni, yorum, süre, tag'ler
- Günlük 10K quota → ~20 arama + ~100 video detail = ~2.1K unit/gün
- Bölge: TR, dil: tr

### Aktif: AI Araç Tespiti (Lokal)
- Video başlık, açıklama ve tag'lerden otomatik AI araç tanıma
- 25+ araç + 60+ alias desteği (Seedance, Kling, Sora, Runway, Veo, Minimax, Pika, Luma vb.)
- False positive filtreleme (Sora=Mobile Legends, Runway=moda, vb.)

### Aktif: Video Sınıflandırma (Lokal)
- "AI ile yapılmış" vs "AI hakkında konuşan" vs "tutorial" ayrımı
- Raporda yapım videoları öncelikli sıralanır

### Opsiyonel: Perplexity Keşif
- `--with-discovery` flag'i ile çalıştırılır
- YouTube'da bulunamayan videoları keşfetme denemesi
- Veri güvenilirliği düşük — tahmini metrikler `~` ile işaretlenir

### Gelecek: X (Twitter) API
- Henüz entegre değil — API maliyeti ($200/ay Basic) nedeniyle ertelendi
- Türkiye'de AI video trendlerinin önemli bir kısmı X'te başlıyor
- Entegre edildiğinde en değerli veri kaynağı olacak

---

## Skorlama Sistemi: VMW Score (Video Market Watch Score)

Her video 0-100 arası skorlanır. Skor bileşenleri:

### Reach Score (0-30 puan)
| Metrik | Ağırlık | Açıklama |
|--------|---------|----------|
| Toplam görüntülenme | %50 | Platformlar arası kümülatif |
| Erişim hızı | %30 | İlk 24/48/72 saat performansı |
| Platformlar arası yayılım | %20 | Kaç platformda mevcut |

### Engagement Score (0-30 puan)
| Metrik | Ağırlık | Açıklama |
|--------|---------|----------|
| Etkileşim oranı | %40 | (beğeni+yorum+paylaşım) / görüntülenme |
| Yorum kalitesi | %30 | Yorum uzunluğu, tartışma derinliği |
| Paylaşım/kaydetme oranı | %30 | Viral yayılım potansiyeli |

### Buzz Score (0-25 puan)
| Metrik | Ağırlık | Açıklama |
|--------|---------|----------|
| Sosyal medya konuşması | %40 | Kaç kez paylaşıldı/bahsedildi |
| Haber medyası kapsamı | %30 | Haber sitelerinde yer alma |
| Topluluk tartışması | %30 | Forum/Reddit/Ekşi konuşmaları |

### Innovation Score (0-15 puan)
| Metrik | Ağırlık | Açıklama |
|--------|---------|----------|
| AI teknik karmaşıklık | %40 | Kullanılan AI araç(lar)ı ve teknik seviye |
| Yaratıcılık | %30 | Konsept özgünlüğü |
| Prodüksiyon kalitesi | %30 | Genel çıktı kalitesi |

---

## Klasör Yapısı

```
@AI Video Market Watch/
├── CLAUDE.md                          # Bu dosya - proje talimatları
├── agent/
│   └── video_market_watch_agent.md    # Ana agent tanımı
│
├── data/
│   ├── tracked_channels.md            # Takip edilen kanal/hesap listesi
│   ├── keyword_library.md             # Arama keyword'leri ve hashtag'ler
│   └── ai_tools_taxonomy.md           # AI araç sınıflandırması
│
├── reports/
│   ├── daily/                         # Günlük takip notları
│   │   └── YYYY-MM-DD.md
│   ├── weekly/                        # Haftalık Top 10 Chart
│   │   └── YYYY-WNN.md
│   └── monthly/                       # Aylık trend raporu
│       └── YYYY-MM.md
│
├── charts/
│   ├── weekly/                        # Haftalık Top 10 HTML chart
│   │   └── YYYY-WNN.html
│   └── monthly/                       # Aylık trend HTML dashboard
│       └── YYYY-MM.html
│
├── insights/
│   ├── viral_breakdowns/              # Viral video detay analizleri
│   │   └── video_slug.md
│   └── trend_patterns/                # Tespit edilen trend pattern'leri
│       └── pattern_name.md
│
└── archive/
    └── hall_of_fame.md                # All-time en başarılı AI videolar
```

---

## Rapor Şablonları

### Günlük Rapor (daily/YYYY-MM-DD.md)
```markdown
# AI Video Market Watch - Günlük Rapor
**Tarih:** YYYY-MM-DD

## Bugün Tespit Edilen Yeni AI Videolar
| # | Video | Platform | Kanal | AI Araç | Görüntülenme | Link |
|---|-------|----------|-------|---------|--------------|------|

## Mevcut Takipteki Videoların Güncel Metrikleri
| # | Video | Platform | Dünkü | Bugünkü | Değişim |
|---|-------|----------|-------|---------|---------|

## Günün Öne Çıkanı
- Video:
- Neden öne çıktı:

## Notlar
-
```

### Haftalık Top 10 Chart (weekly/YYYY-WNN.md)
```markdown
# AI Video Market Watch - Haftalık Top 10
**Hafta:** YYYY-WNN (Tarih Aralığı)

## 🏆 Top 10 Chart

### #1 - [Video Başlığı]
- **VMW Score:** XX/100
- **Platform:** YouTube | Shorts | Reels | TikTok | X
- **Kanal/Hesap:** @xxx
- **AI Araç:** Sora / Runway / Kling / vb.
- **Metrikler:**
  - Görüntülenme: X
  - Beğeni: X
  - Yorum: X
  - Paylaşım: X
- **Link:** [URL]
- **Neden Başarılı:**
  > Kısa analiz paragrafı

(#2-#10 aynı formatta)

## Haftalık Trendler
- En çok kullanılan AI araç:
- En başarılı format:
- En aktif platform:
- Yükselen tema/konu:

## Geçen Haftayla Karşılaştırma
| Metrik | Bu Hafta | Geçen Hafta | Değişim |
|--------|----------|-------------|---------|
```

### Aylık Trend Raporu (monthly/YYYY-MM.md)
```markdown
# AI Video Market Watch - Aylık Trend Raporu
**Ay:** YYYY-MM

## Executive Summary
(3-5 cümle özet)

## Ayın Top 10 (Kümülatif VMW Score)

## Platform Bazlı Analiz
### YouTube
### YouTube Shorts
### Instagram Reels
### TikTok
### X (Twitter)

## AI Araç Trendleri
| AI Araç | Kullanım Sayısı | Ort. VMW Score | Trend |
|---------|-----------------|----------------|-------|

## İçerik Kategorisi Analizi
| Kategori | Adet | Ort. Score | Öne Çıkan Video |
|----------|------|------------|-----------------|

## Öne Çıkan Insight'lar
1.
2.
3.

## Gelecek Ay Tahminleri
-
```

---

## Raporlama Dili

- **Tüm raporlar ve analizler Türkçe** yazılır
- Video başlıkları orijinal dilinde bırakılır
- Teknik terimler (engagement, reach, viral vb.) yaygın kullanıldığı şekliyle İngilizce kalabilir

---

## İş Akışı

### Günlük Rutin
```bash
python3 scripts/run_daily.py                  # Standart tarama
python3 scripts/run_daily.py --with-discovery # Perplexity keşifli
python3 scripts/run_daily.py --date YYYY-MM-DD # Belirli tarih
```
1. YouTube Data API ile keyword araması (10 keyword grubu)
2. Bulunan videoların kesin metriklerini çek
3. AI araç tespiti (başlık/açıklama/tag parsing)
4. Video sınıflandırma (yapım/haber/belirsiz)
5. VMW Score hesapla ve rapor üret

### Haftalık Rutin (Her Pazar)
```bash
python3 scripts/run_weekly.py                 # Bu haftanın Top 10'u
python3 scripts/run_weekly.py --week 2026-W09 # Belirli hafta
```
1. Haftanın günlük JSON verilerini birleştir
2. VMW Score hesapla ve Top 10 sırala
3. Markdown rapor + HTML chart üret
4. Platform ve AI araç dağılımı analizi

### Aylık Rutin (Her ayın 1'i)
1. Tüm haftalık verileri kümülatif olarak değerlendir
2. Aylık Top 10 (en yüksek kümülatif VMW Score)
3. Platform bazlı karşılaştırmalı analiz
4. AI araç trendleri raporu
5. İçerik kategorisi analizi
6. HTML dashboard oluştur
7. Hall of Fame güncellemesi

---

## Kurallar ve İlkeler

1. **Doğruluk:** Metrikler doğrulanabilir kaynaklardan alınmalı, tahmin kullanılacaksa açıkça belirtilmeli
2. **Güncellik:** Veriler en fazla 24 saat eski olmalı (günlük rapor için)
3. **Objektivite:** Skorlama sistemi tutarlı uygulanmalı, kişisel yargı minimize edilmeli
4. **Kapsayıcılık:** Sadece büyük kanallar değil, küçük üreticiler de takip edilmeli
5. **AI Doğrulaması:** "AI ile yapılmış" iddiası mümkün olduğunca doğrulanmalı (video açıklaması, kanal bilgisi, görsel analiz)
6. **Şeffaflık:** Veri kaynakları ve sınırlılıklar her raporda belirtilmeli

import { motion } from 'framer-motion'
import { Link } from 'react-router-dom'
import {
  ArrowRight,
  Youtube,
  Search,
  BarChart3,
  FileText,
  Database,
  Globe,
} from 'lucide-react'

const techStack = [
  {
    icon: Youtube,
    title: 'YouTube Data API v3',
    desc: 'Gunluk 40+ anahtar kelime kombinasyonunda video arama ve metrik toplama. 10K quota/gun.',
  },
  {
    icon: Search,
    title: 'Perplexity AI',
    desc: "YouTube disindaki platformlarda AI video keşfi. Sonar model ile web'i tarama.",
  },
  {
    icon: BarChart3,
    title: 'VMW Scorer',
    desc: '4 boyutlu puanlama: Reach (30), Engagement (30), Buzz (25), Innovation (15).',
  },
  {
    icon: FileText,
    title: 'Report Engine',
    desc: 'Markdown + HTML rapor uretimi. Gunluk, haftalik ve aylik raporlar.',
  },
  {
    icon: Database,
    title: 'JSON Data Store',
    desc: 'Tum video verileri JSON formatinda saklanir. Tarihsel veri arsivi.',
  },
  {
    icon: Globe,
    title: 'Multi-Platform',
    desc: 'YouTube, Instagram Reels, TikTok, X platformlarinda icerik takibi.',
  },
]

const dataSources = [
  {
    name: 'YouTube API',
    type: 'Primary',
    accuracy: '%100 dogrulanmis',
    desc: 'Video metrikleri, kanal bilgisi, detayli istatistikler',
  },
  {
    name: 'Perplexity AI',
    type: 'Secondary',
    accuracy: '~%70 tahmini',
    desc: 'YouTube disi platform keşfi',
  },
  {
    name: 'Manuel Kurasyon',
    type: 'Tertiary',
    accuracy: 'Dogrulanmis',
    desc: 'Takip edilen kanallar listesi',
  },
]

const trackedCreators = [
  {
    tier: 'Tier 1 — Profesyonel Studyolar',
    creators: [
      'Pepper Root Creative AI Studio',
      'Nexor Studio',
      '788 Creative Studio',
      'FUKO Creative',
      'KLOK',
      'Sentetika',
    ],
  },
  {
    tier: 'Tier 2 — Bagimsiz Yaraticilar',
    creators: [
      '@stevedacinema',
      '@ujkatimbu',
      'Diger gelisen yaraticilar',
    ],
  },
  {
    tier: 'Tier 3 — Ajanslar',
    creators: ['VideoSanat', 'FilmUp', 'Diger ajanslar'],
  },
]

export default function About() {
  return (
    <div className="pt-16">
      {/* Header */}
      <section className="bg-bg-alt">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-16 pb-20">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="max-w-3xl"
          >
            <h1 className="text-4xl sm:text-5xl font-extrabold text-primary mb-4 tracking-tight">
              VMW Hakkinda
            </h1>
            <p className="text-lg text-secondary max-w-2xl leading-relaxed">
              AI Video Market Watch, Turkiye'deki AI ile uretilen videolari
              sistematik olarak izleyen, puanlayan ve analiz eden bir market
              intelligence platformudur.
            </p>
          </motion.div>
        </div>
      </section>

      {/* Tech Stack */}
      <section className="py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-2xl font-bold text-primary mb-8">
            Teknik Altyapi
          </h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {techStack.map((t, i) => {
              const Icon = t.icon
              return (
                <motion.div
                  key={t.title}
                  initial={{ opacity: 0, y: 20 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  transition={{ delay: i * 0.1 }}
                  className="bg-surface border border-border rounded-2xl p-6"
                >
                  <div className="w-10 h-10 rounded-xl bg-accent/10 flex items-center justify-center mb-4">
                    <Icon size={20} className="text-accent" />
                  </div>
                  <h3 className="font-bold text-primary mb-2">{t.title}</h3>
                  <p className="text-secondary text-sm leading-relaxed">
                    {t.desc}
                  </p>
                </motion.div>
              )
            })}
          </div>
        </div>
      </section>

      {/* Data Sources */}
      <section className="py-16 bg-bg-alt">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-2xl font-bold text-primary mb-8">
            Veri Kaynaklari
          </h2>
          <div className="bg-surface border border-border rounded-2xl overflow-hidden">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-border bg-bg-alt">
                  <th className="text-left py-4 px-6 font-semibold text-primary">
                    Kaynak
                  </th>
                  <th className="text-center py-4 px-6 font-semibold text-primary">
                    Tip
                  </th>
                  <th className="text-center py-4 px-6 font-semibold text-primary">
                    Dogruluk
                  </th>
                  <th className="text-left py-4 px-6 font-semibold text-primary">
                    Kapsam
                  </th>
                </tr>
              </thead>
              <tbody>
                {dataSources.map((ds) => (
                  <tr key={ds.name} className="border-b border-border/50">
                    <td className="py-4 px-6 font-medium text-primary font-mono">
                      {ds.name}
                    </td>
                    <td className="py-4 px-6 text-center">
                      <span className="text-xs font-mono bg-bg-alt rounded-full px-3 py-1 text-secondary">
                        {ds.type}
                      </span>
                    </td>
                    <td className="py-4 px-6 text-center text-xs text-secondary">
                      {ds.accuracy}
                    </td>
                    <td className="py-4 px-6 text-xs text-secondary">
                      {ds.desc}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </section>

      {/* Tracked Creators */}
      <section className="py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-2xl font-bold text-primary mb-8">
            Takip Edilen Yaraticilar
          </h2>
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {trackedCreators.map((tier, i) => (
              <motion.div
                key={tier.tier}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.1 }}
                className="bg-surface border border-border rounded-2xl p-6"
              >
                <h3 className="font-bold text-primary text-sm mb-4">
                  {tier.tier}
                </h3>
                <ul className="space-y-2">
                  {tier.creators.map((c) => (
                    <li key={c} className="text-sm text-secondary">
                      &bull; {c}
                    </li>
                  ))}
                </ul>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Project Structure */}
      <section className="py-16 bg-bg-alt">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-2xl font-bold text-primary mb-8">
            Proje Yapisi
          </h2>
          <div className="bg-surface border border-border rounded-2xl p-6 sm:p-8 font-mono text-sm">
            <pre className="text-secondary whitespace-pre-wrap leading-relaxed">
              {`video-market-watch/
├── src/                    # React web app
├── scripts/                # Python pipeline scriptleri
│   ├── run_daily.py        # Gunluk orkestrator
│   ├── run_weekly.py       # Haftalik chart
│   ├── youtube_metrics.py  # YouTube API entegrasyonu
│   ├── discovery.py        # Perplexity AI keşfi
│   ├── scorer.py           # VMW Score hesaplayici
│   ├── report_generator.py # Rapor uretici
│   ├── email_sender.py     # E-posta dagitimi
│   ├── social_scanner.py   # Sosyal medya taramasi
│   └── config.py           # Yapilandirma
├── data/                   # Toplanan veriler (JSON)
├── reports/                # Uretilen raporlar
│   ├── daily/              # Gunluk raporlar
│   └── weekly/             # Haftalik chartlar
├── charts/                 # HTML gorselleştirmeler
├── insights/               # Trend analizleri
├── logs/                   # Calisma kayitlari
└── archive/                # Hall of Fame & viral analizler`}
            </pre>
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-20 bg-primary">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl font-extrabold text-white mb-4">
            VMW Score Sistemini Inceleyin
          </h2>
          <p className="text-white/60 max-w-xl mx-auto mb-8">
            Reach, Engagement, Buzz ve Innovation boyutlarinda nasil
            puanlandigini detayli ogrenin.
          </p>
          <Link
            to="/scoring"
            className="inline-flex items-center gap-2 bg-accent text-white px-8 py-3.5 rounded-full font-semibold text-sm no-underline hover:bg-accent/90 transition-colors"
          >
            Puanlama Sistemi
            <ArrowRight size={16} />
          </Link>
        </div>
      </section>
    </div>
  )
}

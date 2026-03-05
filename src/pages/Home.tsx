import { motion } from 'framer-motion'
import { Link } from 'react-router-dom'
import {
  ArrowRight,
  Play,
  BarChart3,
  Search,
  TrendingUp,
  Zap,
  Eye,
  Globe,
} from 'lucide-react'
import { pipelineSteps } from '../data/pipeline'
import { scoreDimensions } from '../data/scoring'

const stats = [
  { label: 'AI Araci Takibi', value: '25+', icon: Zap },
  { label: 'Anahtar Kelime', value: '40+', icon: Search },
  { label: 'Gunluk Tarama', value: '7/24', icon: Eye },
  { label: 'Platform', value: '5+', icon: Globe },
]

export default function Home() {
  return (
    <div className="pt-16">
      {/* Hero */}
      <section className="bg-bg-alt">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-20 pb-24">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="max-w-3xl"
          >
            <div className="inline-flex items-center gap-2 bg-surface border border-border rounded-full px-4 py-2 mb-6">
              <Play size={14} className="text-accent" fill="#FF3B30" />
              <span className="text-sm text-secondary">
                AI Video Market Intelligence — Turkiye
              </span>
            </div>
            <h1 className="text-4xl sm:text-6xl font-extrabold tracking-tight mb-6">
              <span className="text-primary">Turkiye AI Video</span>
              <br />
              <span className="gradient-text">Ekosistemini Takip Edin</span>
            </h1>
            <p className="text-lg text-secondary max-w-2xl leading-relaxed mb-8">
              VMW, Turkiye'deki AI ile uretilen videolari gunluk olarak tarar,
              puanlar ve analiz eder. YouTube, Instagram, TikTok ve diger
              platformlardaki viral AI iceriklerini izleyin.
            </p>
            <div className="flex flex-wrap gap-3">
              <Link
                to="/pipeline"
                className="inline-flex items-center gap-2 bg-accent text-white px-6 py-3 rounded-full font-semibold text-sm no-underline hover:bg-accent/90 transition-colors"
              >
                Pipeline'i Incele
                <ArrowRight size={16} />
              </Link>
              <Link
                to="/scoring"
                className="inline-flex items-center gap-2 bg-surface border border-border text-primary px-6 py-3 rounded-full font-semibold text-sm no-underline hover:bg-bg-alt transition-colors"
              >
                VMW Score
                <BarChart3 size={16} />
              </Link>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Stats */}
      <section className="py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
            {stats.map((s, i) => {
              const Icon = s.icon
              return (
                <motion.div
                  key={s.label}
                  initial={{ opacity: 0, y: 20 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  transition={{ delay: i * 0.1 }}
                  className="bg-surface border border-border rounded-2xl p-6 text-center card-hover"
                >
                  <Icon size={20} className="mx-auto mb-3 text-accent" />
                  <div className="text-3xl font-extrabold text-primary mb-1">
                    {s.value}
                  </div>
                  <div className="text-sm text-secondary">{s.label}</div>
                </motion.div>
              )
            })}
          </div>
        </div>
      </section>

      {/* Pipeline Overview */}
      <section className="py-16 bg-bg-alt">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-2xl font-bold text-primary mb-2">
            Gunluk Pipeline
          </h2>
          <p className="text-secondary text-sm mb-8">
            Her gun otomatik calisan 5 adimlik veri toplama ve analiz sureci.
          </p>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4">
            {pipelineSteps.map((step, i) => {
              const Icon = step.icon
              return (
                <motion.div
                  key={step.id}
                  initial={{ opacity: 0, y: 20 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  transition={{ delay: i * 0.1 }}
                  className="bg-surface border border-border rounded-2xl p-5 card-hover"
                >
                  <div
                    className="w-10 h-10 rounded-xl flex items-center justify-center mb-3"
                    style={{ backgroundColor: step.colorLight }}
                  >
                    <Icon size={18} style={{ color: step.color }} />
                  </div>
                  <div className="text-xs font-mono text-secondary mb-1">
                    Adim {step.id}
                  </div>
                  <h3 className="font-bold text-primary text-sm">
                    {step.name}
                  </h3>
                </motion.div>
              )
            })}
          </div>
          <div className="mt-6 text-center">
            <Link
              to="/pipeline"
              className="text-accent text-sm font-semibold no-underline hover:underline inline-flex items-center gap-1"
            >
              Detayli Pipeline <ArrowRight size={14} />
            </Link>
          </div>
        </div>
      </section>

      {/* VMW Score */}
      <section className="py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-2xl font-bold text-primary mb-2">VMW Score</h2>
          <p className="text-secondary text-sm mb-8">
            Her video 4 boyutta degerlendirilir, toplam 100 puan uzerinden.
          </p>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            {scoreDimensions.map((dim, i) => (
              <motion.div
                key={dim.name}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.1 }}
                className="bg-surface border border-border rounded-2xl p-6 card-hover"
              >
                <div className="flex items-center justify-between mb-3">
                  <h3 className="font-bold text-primary">{dim.name}</h3>
                  <span
                    className="text-xs font-mono font-bold px-2.5 py-1 rounded-full"
                    style={{
                      backgroundColor: dim.color + '20',
                      color: dim.color,
                    }}
                  >
                    /{dim.maxScore}
                  </span>
                </div>
                <p className="text-secondary text-sm mb-3">
                  {dim.description}
                </p>
                <div
                  className="h-1.5 rounded-full"
                  style={{ backgroundColor: dim.color + '20' }}
                >
                  <div
                    className="h-full rounded-full"
                    style={{
                      backgroundColor: dim.color,
                      width: `${(dim.maxScore / 30) * 100}%`,
                    }}
                  />
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="py-16 bg-bg-alt">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-2xl font-bold text-primary mb-8">
            Temel Ozellikler
          </h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {[
              {
                icon: Search,
                title: 'Akilli Video Keşfi',
                desc: 'YouTube API + Perplexity AI ile 40+ anahtar kelime kombinasyonunda gunluk tarama.',
              },
              {
                icon: Zap,
                title: 'AI Arac Tespiti',
                desc: '25+ AI aracini otomatik tespit. False-positive filtreleme ile yuksek dogruluk.',
              },
              {
                icon: BarChart3,
                title: 'VMW Scoring',
                desc: 'Reach, Engagement, Buzz ve Innovation boyutlarinda 0-100 puanlama.',
              },
              {
                icon: TrendingUp,
                title: 'Trend Analizi',
                desc: 'Haftalik Top 10, aylik trendler, Hall of Fame takibi.',
              },
              {
                icon: Globe,
                title: 'Multi-Platform',
                desc: 'YouTube, Instagram Reels, TikTok, X platformlarinda takip.',
              },
              {
                icon: Eye,
                title: 'Tracker Channels',
                desc: 'Profesyonel AI video studyolari ve bagimsiz yaraticilar.',
              },
            ].map((f, i) => {
              const Icon = f.icon
              return (
                <motion.div
                  key={f.title}
                  initial={{ opacity: 0, y: 20 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  transition={{ delay: i * 0.08 }}
                  className="bg-surface border border-border rounded-2xl p-6"
                >
                  <div className="w-10 h-10 rounded-xl bg-accent/10 flex items-center justify-center mb-4">
                    <Icon size={20} className="text-accent" />
                  </div>
                  <h3 className="font-bold text-primary mb-2">{f.title}</h3>
                  <p className="text-secondary text-sm leading-relaxed">
                    {f.desc}
                  </p>
                </motion.div>
              )
            })}
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-20 bg-primary">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl font-extrabold text-white mb-4">
            AI Video Trendlerini Kacirmayin
          </h2>
          <p className="text-white/60 max-w-xl mx-auto mb-8">
            Puanlama sistemini, takip edilen AI araclarini ve pipeline'i
            detayli inceleyin.
          </p>
          <div className="flex flex-wrap gap-3 justify-center">
            <Link
              to="/scoring"
              className="inline-flex items-center gap-2 bg-accent text-white px-8 py-3.5 rounded-full font-semibold text-sm no-underline hover:bg-accent/90 transition-colors"
            >
              VMW Score
              <BarChart3 size={16} />
            </Link>
            <Link
              to="/tools"
              className="inline-flex items-center gap-2 bg-white text-primary px-8 py-3.5 rounded-full font-semibold text-sm no-underline hover:bg-white/90 transition-colors"
            >
              AI Araclari
              <ArrowRight size={16} />
            </Link>
          </div>
        </div>
      </section>
    </div>
  )
}

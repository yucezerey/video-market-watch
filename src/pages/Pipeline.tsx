import { motion } from 'framer-motion'
import { CheckCircle2, Terminal, Clock, ArrowRight } from 'lucide-react'
import { pipelineSteps, orchestrator } from '../data/pipeline'

export default function Pipeline() {
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
            <div className="inline-flex items-center gap-2 bg-surface border border-border rounded-full px-4 py-2 mb-6">
              <span className="text-sm text-secondary">
                5 Adimlik Gunluk Pipeline
              </span>
            </div>
            <h1 className="text-4xl sm:text-5xl font-extrabold text-primary mb-4 tracking-tight">
              VMW Pipeline
            </h1>
            <p className="text-lg text-secondary max-w-2xl leading-relaxed">
              Her gun otomatik calisan veri toplama, analiz ve raporlama
              sureci. YouTube API + Perplexity AI + VMW Scoring entegrasyonu.
            </p>
          </motion.div>
        </div>
      </section>

      {/* Orchestrator */}
      <section className="py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-2xl font-bold text-primary mb-8">
            Orkestrator
          </h2>
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="bg-accent/5 border border-accent/20 rounded-2xl p-6 sm:p-8"
          >
            <div className="flex items-start gap-4">
              <div className="w-12 h-12 rounded-xl bg-accent/10 flex items-center justify-center shrink-0">
                <Terminal size={22} className="text-accent" />
              </div>
              <div>
                <h3 className="font-bold text-primary text-lg mb-1">
                  {orchestrator.name}
                </h3>
                <p className="text-secondary text-sm mb-4">
                  {orchestrator.description}
                </p>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                  {orchestrator.steps.map((step, i) => (
                    <div
                      key={step}
                      className="flex items-center gap-2 text-sm text-primary"
                    >
                      <span className="w-5 h-5 rounded-full bg-accent/10 text-accent flex items-center justify-center text-xs font-bold shrink-0">
                        {i + 1}
                      </span>
                      {step}
                    </div>
                  ))}
                </div>
                <div className="mt-4 flex items-center gap-2 text-xs text-secondary">
                  <Clock size={12} />
                  <span>vmw-daily.sh ile her gun otomatik tetiklenir</span>
                </div>
              </div>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Pipeline Steps */}
      <section className="py-16 bg-bg-alt">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-2xl font-bold text-primary mb-12">
            Pipeline Adimlari
          </h2>
          <div className="max-w-3xl space-y-8">
            {pipelineSteps.map((step, i) => {
              const Icon = step.icon
              return (
                <motion.div
                  key={step.id}
                  initial={{ opacity: 0, x: -20 }}
                  whileInView={{ opacity: 1, x: 0 }}
                  viewport={{ once: true }}
                  transition={{ delay: i * 0.1 }}
                  className="relative"
                >
                  {i < pipelineSteps.length - 1 && (
                    <div
                      className="absolute left-6 top-16 w-0.5 h-full -mb-8"
                      style={{ backgroundColor: step.color + '30' }}
                    />
                  )}
                  <div className="bg-surface border border-border rounded-2xl p-6 relative">
                    <div className="flex items-start gap-4">
                      <div
                        className="w-12 h-12 rounded-xl flex items-center justify-center shrink-0"
                        style={{ backgroundColor: step.colorLight }}
                      >
                        <Icon size={20} style={{ color: step.color }} />
                      </div>
                      <div className="flex-1">
                        <div className="flex items-center gap-2 mb-1">
                          <span
                            className="text-xs font-mono font-medium px-2 py-0.5 rounded-full"
                            style={{
                              backgroundColor: step.colorLight,
                              color: step.color,
                            }}
                          >
                            Adim {step.id}
                          </span>
                          <h3 className="font-bold text-primary">
                            {step.name}
                          </h3>
                        </div>
                        <p className="text-sm text-secondary mb-3">
                          {step.title}
                        </p>
                        <p className="text-sm text-secondary mb-4 leading-relaxed">
                          {step.description}
                        </p>

                        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                          <div>
                            <h4 className="text-xs font-semibold text-secondary uppercase tracking-wider mb-2">
                              Scriptler
                            </h4>
                            {step.scripts.map((s) => (
                              <div
                                key={s}
                                className="text-xs font-mono bg-bg-alt rounded-lg px-3 py-1.5 mb-1 text-primary"
                              >
                                {s}
                              </div>
                            ))}
                          </div>
                          <div>
                            <h4 className="text-xs font-semibold text-secondary uppercase tracking-wider mb-2">
                              Ciktilar
                            </h4>
                            {step.outputs.map((o) => (
                              <div
                                key={o}
                                className="flex items-center gap-1.5 text-xs text-secondary mb-1"
                              >
                                <CheckCircle2
                                  size={12}
                                  style={{ color: step.color }}
                                />
                                {o}
                              </div>
                            ))}
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </motion.div>
              )
            })}
          </div>
        </div>
      </section>

      {/* Data Flow */}
      <section className="py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-2xl font-bold text-primary mb-8">
            Rapor Tipleri
          </h2>
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
            {[
              {
                title: 'Gunluk Rapor',
                freq: 'Her gun',
                items: [
                  'Top 10 video siralaması',
                  'Tam video listesi + metrikler',
                  'Veri kaynagi seffafligi',
                  'HTML dashboard',
                ],
                color: '#FF3B30',
              },
              {
                title: 'Haftalik Chart',
                freq: 'Pazar gunleri',
                items: [
                  'Haftalik Top 10 (madalya)',
                  'Platform dagilim analizi',
                  'AI arac kullanim istatistikleri',
                  'Hafta-hafta karsilastirma',
                ],
                color: '#5E5CE6',
              },
              {
                title: 'Aylik Trend',
                freq: 'Ay sonu',
                items: [
                  'Aylik Top 10 (kumulatif VMW)',
                  'Platform ozel analizler',
                  'AI arac trend analizi',
                  'Tahmin ve ongoru',
                ],
                color: '#FF9500',
              },
            ].map((report, i) => (
              <motion.div
                key={report.title}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.1 }}
                className="bg-surface border border-border rounded-2xl p-6"
              >
                <div className="flex items-center gap-2 mb-3">
                  <div
                    className="w-2.5 h-2.5 rounded-full"
                    style={{ backgroundColor: report.color }}
                  />
                  <h3 className="font-bold text-primary">{report.title}</h3>
                </div>
                <span className="text-xs font-mono text-secondary">
                  {report.freq}
                </span>
                <ul className="mt-3 space-y-2">
                  {report.items.map((item) => (
                    <li
                      key={item}
                      className="flex items-start gap-2 text-sm text-secondary"
                    >
                      <ArrowRight
                        size={12}
                        className="mt-0.5 shrink-0"
                        style={{ color: report.color }}
                      />
                      {item}
                    </li>
                  ))}
                </ul>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Usage */}
      <section className="py-16 bg-bg-alt">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-2xl font-bold text-primary mb-8">Kullanim</h2>
          <div className="bg-surface border border-border rounded-2xl p-6 font-mono text-sm">
            <div className="space-y-2 text-secondary">
              <div className="text-primary font-semibold">
                # Gunluk tarama
              </div>
              <code className="block bg-bg-alt rounded-xl px-4 py-2">
                python scripts/run_daily.py
              </code>
              <div className="text-primary font-semibold mt-4">
                # Haftalik chart olusturma
              </div>
              <code className="block bg-bg-alt rounded-xl px-4 py-2">
                python scripts/run_weekly.py
              </code>
              <div className="text-primary font-semibold mt-4">
                # Otomatik cron (her gun)
              </div>
              <code className="block bg-bg-alt rounded-xl px-4 py-2">
                bash scripts/vmw-daily.sh
              </code>
            </div>
          </div>
        </div>
      </section>
    </div>
  )
}

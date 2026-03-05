import { motion } from 'framer-motion'
import { scoreDimensions, scoreLevels, keywords } from '../data/scoring'

export default function Scoring() {
  const totalMax = scoreDimensions.reduce((sum, d) => sum + d.maxScore, 0)

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
              VMW Score Sistemi
            </h1>
            <p className="text-lg text-secondary max-w-2xl leading-relaxed">
              Her AI video 4 boyutta degerlendirilir: Reach, Engagement, Buzz
              ve Innovation. Toplam VMW Score 0-{totalMax} arasi.
            </p>
          </motion.div>
        </div>
      </section>

      {/* Score Dimensions */}
      <section className="py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-2xl font-bold text-primary mb-8">
            Skor Boyutlari
          </h2>

          <div className="bg-surface border border-border rounded-2xl overflow-hidden mb-8">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-border bg-bg-alt">
                  <th className="text-left py-4 px-6 font-semibold text-primary">
                    Boyut
                  </th>
                  <th className="text-center py-4 px-6 font-semibold text-primary">
                    Maks. Puan
                  </th>
                  <th className="text-left py-4 px-6 font-semibold text-primary">
                    Metrikler
                  </th>
                </tr>
              </thead>
              <tbody>
                {scoreDimensions.map((dim) => (
                  <tr key={dim.name} className="border-b border-border/50">
                    <td className="py-4 px-6">
                      <div className="flex items-center gap-3">
                        <div
                          className="w-3 h-3 rounded-full"
                          style={{ backgroundColor: dim.color }}
                        />
                        <span className="font-medium text-primary">
                          {dim.name}
                        </span>
                      </div>
                    </td>
                    <td className="py-4 px-6 text-center">
                      <span
                        className="text-xs font-mono font-medium px-3 py-1 rounded-full"
                        style={{
                          backgroundColor: dim.color + '20',
                          color: dim.color,
                        }}
                      >
                        /{dim.maxScore}
                      </span>
                    </td>
                    <td className="py-4 px-6">
                      <ul className="space-y-1">
                        {dim.metrics.map((m) => (
                          <li key={m} className="text-xs text-secondary">
                            &bull; {m}
                          </li>
                        ))}
                      </ul>
                    </td>
                  </tr>
                ))}
                <tr className="border-t-2 border-primary bg-primary/5">
                  <td className="py-4 px-6 font-bold text-primary">
                    TOPLAM VMW SCORE
                  </td>
                  <td className="py-4 px-6 text-center font-bold font-mono text-accent">
                    /{totalMax}
                  </td>
                  <td className="py-4 px-6 text-sm text-secondary">
                    Agirlikli toplam
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          {/* Weight bar */}
          <div className="bg-surface border border-border rounded-2xl p-6">
            <h3 className="text-sm font-semibold text-primary mb-4">
              Puan Dagilimi
            </h3>
            <div className="flex rounded-full overflow-hidden h-8">
              {scoreDimensions.map((dim) => (
                <div
                  key={dim.name}
                  className="flex items-center justify-center text-white text-xs font-mono font-medium"
                  style={{
                    backgroundColor: dim.color,
                    width: `${(dim.maxScore / totalMax) * 100}%`,
                  }}
                  title={`${dim.name}: ${dim.maxScore}`}
                >
                  {dim.maxScore}
                </div>
              ))}
            </div>
            <div className="flex flex-wrap gap-3 mt-4">
              {scoreDimensions.map((dim) => (
                <div
                  key={dim.name}
                  className="flex items-center gap-1.5 text-xs text-secondary"
                >
                  <div
                    className="w-2.5 h-2.5 rounded-full"
                    style={{ backgroundColor: dim.color }}
                  />
                  {dim.name} ({dim.maxScore})
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Score Levels */}
      <section className="py-16 bg-bg-alt">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-2xl font-bold text-primary mb-8">
            Skor Seviyeleri
          </h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4">
            {scoreLevels.map((level, i) => (
              <motion.div
                key={level.range}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.1 }}
                className="bg-surface border border-border rounded-2xl p-5 text-center"
              >
                <div className="text-2xl mb-2">{level.emoji}</div>
                <div className="text-lg font-bold text-primary mb-1">
                  {level.range}
                </div>
                <div className="text-sm font-semibold text-primary mb-2">
                  {level.label}
                </div>
                <p className="text-xs text-secondary">{level.desc}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Keywords */}
      <section className="py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-2xl font-bold text-primary mb-2">
            Arama Anahtar Kelimeleri
          </h2>
          <p className="text-secondary text-sm mb-6">
            YouTube API ve Perplexity ile taranan 40+ kelime kombinasyonundan
            ornekler.
          </p>
          <div className="flex flex-wrap gap-2">
            {keywords.map((kw) => (
              <span
                key={kw}
                className="text-xs font-mono bg-surface border border-border rounded-full px-3 py-1.5 text-secondary"
              >
                {kw}
              </span>
            ))}
          </div>
        </div>
      </section>
    </div>
  )
}

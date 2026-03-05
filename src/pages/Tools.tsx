import { useState } from 'react'
import { motion } from 'framer-motion'
import { aiTools, toolCategories } from '../data/tools'

export default function Tools() {
  const [activeCategory, setActiveCategory] = useState<string | null>(null)

  const filtered = activeCategory
    ? aiTools.filter((t) => t.category === activeCategory)
    : aiTools

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
                {aiTools.length} AI Araci Takipte
              </span>
            </div>
            <h1 className="text-4xl sm:text-5xl font-extrabold text-primary mb-4 tracking-tight">
              Takip Edilen AI Araclari
            </h1>
            <p className="text-lg text-secondary max-w-2xl leading-relaxed">
              VMW'nin videolarda otomatik tespit ettigi AI araclari. Video
              uretim, gorsel uretim, ses/muzik ve yardimci AI kategorilerinde.
            </p>
          </motion.div>
        </div>
      </section>

      {/* Filters */}
      <section className="sticky top-16 z-40 glass border-b border-border">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex flex-wrap gap-2">
            <button
              onClick={() => setActiveCategory(null)}
              className={`px-4 py-2 rounded-full text-sm font-medium transition-colors ${
                !activeCategory
                  ? 'bg-primary text-white'
                  : 'bg-bg-alt text-secondary hover:text-primary'
              }`}
            >
              Tumu ({aiTools.length})
            </button>
            {toolCategories.map((c) => (
              <button
                key={c.id}
                onClick={() =>
                  setActiveCategory(activeCategory === c.id ? null : c.id)
                }
                className={`px-4 py-2 rounded-full text-sm font-medium transition-colors ${
                  activeCategory === c.id
                    ? 'text-white'
                    : 'bg-bg-alt text-secondary hover:text-primary'
                }`}
                style={
                  activeCategory === c.id
                    ? { backgroundColor: c.color }
                    : undefined
                }
              >
                {c.label} ({c.count})
              </button>
            ))}
          </div>
        </div>
      </section>

      {/* Tools Grid */}
      <section className="py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            {filtered.map((tool, i) => (
              <motion.div
                key={tool.name}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: (i % 8) * 0.05 }}
                className="bg-surface border border-border rounded-2xl p-5 card-hover"
              >
                <div className="flex items-center gap-3 mb-3">
                  <div
                    className="w-10 h-10 rounded-xl flex items-center justify-center text-white font-bold text-sm"
                    style={{ backgroundColor: tool.color }}
                  >
                    {tool.name.substring(0, 2).toUpperCase()}
                  </div>
                  <div>
                    <h3 className="font-bold text-primary text-sm">
                      {tool.name}
                    </h3>
                    <span
                      className="text-xs font-mono px-2 py-0.5 rounded-full"
                      style={{
                        backgroundColor:
                          toolCategories.find((c) => c.id === tool.category)
                            ?.color + '20',
                        color: toolCategories.find(
                          (c) => c.id === tool.category,
                        )?.color,
                      }}
                    >
                      {
                        toolCategories.find((c) => c.id === tool.category)
                          ?.label
                      }
                    </span>
                  </div>
                </div>
                <p className="text-secondary text-sm">{tool.description}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Detection Info */}
      <section className="py-16 bg-bg-alt">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-2xl font-bold text-primary mb-8">
            AI Arac Tespit Sistemi
          </h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {[
              {
                title: 'Otomatik Tespit',
                desc: 'Video basligi, aciklamasi ve etiketlerinde AI arac isimlerini otomatik tarar.',
              },
              {
                title: 'False-Positive Filtreleme',
                desc: '"Sora" (oyun karakteri) vs "Sora" (AI araci) gibi cakismalari akilli filtreleme ile ayirt eder.',
              },
              {
                title: 'Video Siniflandirma',
                desc: 'Her video ai_made (AI ile yapilmis), ai_about (AI hakkinda), ai_tutorial (ogretici) veya uncertain olarak siniflandirilir.',
              },
              {
                title: 'Coklu Arac Tespiti',
                desc: 'Bir videoda birden fazla AI araci kullanilmissa hepsi ayri ayri tespit edilir.',
              },
              {
                title: 'Baglam Dogrulama',
                desc: 'Kisa anahtar kelimeler (Wan, Flux gibi) icin ekstra baglam kontrolu yapilir.',
              },
              {
                title: 'Surekli Guncelleme',
                desc: 'Yeni AI araclari piyasaya ciktikca tespit listesi guncellenir.',
              },
            ].map((f, i) => (
              <motion.div
                key={f.title}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.08 }}
                className="bg-surface border border-border rounded-2xl p-6"
              >
                <h3 className="font-bold text-primary text-sm mb-2">
                  {f.title}
                </h3>
                <p className="text-secondary text-sm leading-relaxed">
                  {f.desc}
                </p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>
    </div>
  )
}

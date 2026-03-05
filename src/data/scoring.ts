export interface ScoreDimension {
  name: string
  maxScore: number
  color: string
  metrics: string[]
  description: string
}

export const scoreDimensions: ScoreDimension[] = [
  {
    name: 'Reach',
    maxScore: 30,
    color: '#FF3B30',
    description: 'Videonun erisim gucu ve yayilma hizi',
    metrics: [
      'Goruntulenme sayisi ve hizi',
      'Platform-arasi erisim',
      'Viral velocity (kritik kitleye ulasma suresi)',
    ],
  },
  {
    name: 'Engagement',
    maxScore: 30,
    color: '#5E5CE6',
    description: 'Izleyici etkilesim kalitesi ve yogunlugu',
    metrics: [
      'Begeni / yorum / paylasim orani',
      'Yorum kalitesi ve derinligi',
      'Kaydetme / paylasma sinyalleri',
    ],
  },
  {
    name: 'Buzz',
    maxScore: 25,
    color: '#FF9500',
    description: 'Sosyal medya ve medya yansimasi',
    metrics: [
      'Sosyal medya bahsedilmeleri',
      'Haber ve basin yansimasi',
      'Topluluk tartismalari (Reddit, Eksi vb.)',
    ],
  },
  {
    name: 'Innovation',
    maxScore: 15,
    color: '#34C759',
    description: 'Teknik yenilikcilik ve yaraticilik',
    metrics: [
      'AI arac karmasikligi',
      'Yaratici vizyon ve ozgunluk',
      'Produksiyon kalitesi',
    ],
  },
]

export const scoreLevels = [
  { range: '75-100', label: 'Viral Hit', emoji: '🏆', color: '#FFD700', desc: 'Hall of Fame seviyesi' },
  { range: '50-74', label: 'Trend', emoji: '🔥', color: '#FF3B30', desc: 'Genis kitlelere ulasan icerik' },
  { range: '30-49', label: 'Notable', emoji: '⭐', color: '#FF9500', desc: 'Dikkate deger performans' },
  { range: '15-29', label: 'Emerging', emoji: '🌱', color: '#34C759', desc: 'Gelisen icerik' },
  { range: '0-14', label: 'Tracked', emoji: '📊', color: '#8E8E93', desc: 'Takip edilen' },
]

export const keywords = [
  'yapay zeka video', 'AI ile yapilan video', 'yapay zeka film',
  'sora video', 'runway video', 'kling video', 'seedance video',
  'minimax video', 'pika video', 'luma video', 'veo video',
  '#yapayzekavideosu', '#aiileyapildi', '#aifilm', '#aivideo',
  'AI kisa film Turkce', 'yapay zeka reklam', 'AI muzik videosu',
]

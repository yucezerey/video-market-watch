import { Search, BarChart3, FileText, Mail, type LucideIcon } from 'lucide-react'

export interface PipelineStep {
  id: number
  name: string
  title: string
  icon: LucideIcon
  color: string
  colorLight: string
  description: string
  scripts: string[]
  outputs: string[]
}

export const pipelineSteps: PipelineStep[] = [
  {
    id: 1,
    name: 'Video Discovery',
    title: 'YouTube API + Perplexity Taramasi',
    icon: Search,
    color: '#FF3B30',
    colorLight: '#FF3B3020',
    description:
      'YouTube Data API v3 ile 40+ anahtar kelime kombinasyonunda arama yapilir. Perplexity AI ile YouTube disindaki platformlardaki videolar kesfedilir.',
    scripts: ['youtube_metrics.py', 'discovery.py'],
    outputs: ['youtube_YYYY-MM-DD.json', 'discovery_YYYY-MM-DD.json'],
  },
  {
    id: 2,
    name: 'AI Tool Detection',
    title: 'Yapay Zeka Araci Tespiti',
    icon: Search,
    color: '#5E5CE6',
    colorLight: '#5E5CE620',
    description:
      '25+ AI aracinin (Sora, Runway, Kling, Seedance, Minimax, Pika vb.) video basliklarinda, aciklamalarinda ve etiketlerinde tespiti yapilir. False-positive filtreleme ile yuksek dogruluk.',
    scripts: ['youtube_metrics.py (detect_ai_tools)'],
    outputs: ['ai_tools listesi per video'],
  },
  {
    id: 3,
    name: 'VMW Scoring',
    title: 'VMW Skor Hesaplamasi (0-100)',
    icon: BarChart3,
    color: '#FF9500',
    colorLight: '#FF950020',
    description:
      'Her video 4 boyutta puanlanir: Reach (0-30), Engagement (0-30), Buzz (0-25), Innovation (0-15). Toplam VMW Score 0-100 arasi.',
    scripts: ['scorer.py'],
    outputs: ['all_videos_YYYY-MM-DD.json'],
  },
  {
    id: 4,
    name: 'Report Generation',
    title: 'Rapor ve Gorselleştirme',
    icon: FileText,
    color: '#34C759',
    colorLight: '#34C75920',
    description:
      'Gunluk Top 10 raporu, haftalik chart, aylik trend analizi olusturulur. Interaktif HTML dashboard ile Apple-style gorselleştirme.',
    scripts: ['report_generator.py'],
    outputs: ['daily/YYYY-MM-DD.md', 'weekly/YYYY-WNN.md', 'charts/*.html'],
  },
  {
    id: 5,
    name: 'Distribution',
    title: 'Dagitim ve Bildirim',
    icon: Mail,
    color: '#AF52DE',
    colorLight: '#AF52DE20',
    description:
      'Olusturulan raporlar e-posta ile dagitilir, sosyal medya ozetleri hazirlanir. Gmail SMTP ile otomatik gonderim.',
    scripts: ['email_sender.py', 'social_scanner.py'],
    outputs: ['E-posta raporu', 'Sosyal medya ozeti'],
  },
]

export const orchestrator = {
  name: 'run_daily.py',
  description:
    'Tum pipeline adimlarini sirasiyla calistiran ana orkestrator. Her gun otomatik olarak vmw-daily.sh uzerinden tetiklenir.',
  steps: [
    'YouTube API taramasi (40+ keyword)',
    'Perplexity discovery (opsiyonel)',
    'AI tool tespiti ve siniflandirma',
    'VMW Score hesaplamasi',
    'Rapor uretimi (MD + HTML)',
    'E-posta dagitimi',
  ],
}

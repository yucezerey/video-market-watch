import { Link } from 'react-router-dom'
import { Play } from 'lucide-react'

export default function Footer() {
  return (
    <footer className="border-t border-border bg-bg-alt py-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div>
            <div className="flex items-center gap-2 mb-3">
              <div className="w-7 h-7 rounded-lg bg-accent flex items-center justify-center">
                <Play size={12} className="text-white ml-0.5" fill="white" />
              </div>
              <span className="font-bold text-primary text-sm">
                AI Video Market Watch
              </span>
            </div>
            <p className="text-secondary text-sm leading-relaxed">
              Turkiye AI video ekosistemini takip eden market intelligence platformu.
            </p>
          </div>

          <div>
            <h4 className="font-semibold text-primary text-sm mb-3">Platform</h4>
            <ul className="space-y-2">
              {[
                { to: '/pipeline', label: 'Pipeline' },
                { to: '/scoring', label: 'VMW Scoring' },
                { to: '/tools', label: 'AI Araclari' },
                { to: '/about', label: 'Hakkinda' },
              ].map((link) => (
                <li key={link.to}>
                  <Link
                    to={link.to}
                    className="text-secondary text-sm no-underline hover:text-primary transition-colors"
                  >
                    {link.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          <div>
            <h4 className="font-semibold text-primary text-sm mb-3">
              Veri Kaynaklari
            </h4>
            <ul className="space-y-2 text-secondary text-sm">
              <li>YouTube Data API v3</li>
              <li>Perplexity AI Search</li>
              <li>Sosyal Medya Taramasi</li>
              <li>Topluluk Takibi</li>
            </ul>
          </div>
        </div>

        <div className="mt-8 pt-6 border-t border-border text-center text-xs text-secondary">
          VMW — AI Video Market Watch &copy; {new Date().getFullYear()}
        </div>
      </div>
    </footer>
  )
}

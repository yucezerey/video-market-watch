import { useState } from 'react'
import { Link, useLocation } from 'react-router-dom'
import { Menu, X, Play } from 'lucide-react'

const navItems = [
  { path: '/', label: 'Ana Sayfa' },
  { path: '/pipeline', label: 'Pipeline' },
  { path: '/scoring', label: 'Puanlama' },
  { path: '/tools', label: 'AI Araclari' },
  { path: '/about', label: 'Hakkinda' },
]

export default function Navbar() {
  const [open, setOpen] = useState(false)
  const { pathname } = useLocation()

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 glass border-b border-border">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <Link to="/" className="flex items-center gap-2 no-underline">
            <div className="w-8 h-8 rounded-lg bg-accent flex items-center justify-center">
              <Play size={14} className="text-white ml-0.5" fill="white" />
            </div>
            <span className="font-bold text-primary text-sm tracking-tight">
              VMW
            </span>
          </Link>

          <div className="hidden md:flex items-center gap-1">
            {navItems.map((item) => (
              <Link
                key={item.path}
                to={item.path}
                className={`px-3 py-2 rounded-lg text-sm font-medium no-underline transition-colors ${
                  pathname === item.path
                    ? 'bg-primary text-white'
                    : 'text-secondary hover:text-primary hover:bg-bg-alt'
                }`}
              >
                {item.label}
              </Link>
            ))}
          </div>

          <button
            onClick={() => setOpen(!open)}
            className="md:hidden p-2 text-secondary"
          >
            {open ? <X size={20} /> : <Menu size={20} />}
          </button>
        </div>
      </div>

      {open && (
        <div className="md:hidden glass border-t border-border">
          <div className="px-4 py-3 space-y-1">
            {navItems.map((item) => (
              <Link
                key={item.path}
                to={item.path}
                onClick={() => setOpen(false)}
                className={`block px-3 py-2 rounded-lg text-sm font-medium no-underline ${
                  pathname === item.path
                    ? 'bg-primary text-white'
                    : 'text-secondary hover:text-primary'
                }`}
              >
                {item.label}
              </Link>
            ))}
          </div>
        </div>
      )}
    </nav>
  )
}

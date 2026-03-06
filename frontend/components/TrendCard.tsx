import type { Trend } from '../pages/index'

interface Props {
  trend: Trend
  index: number
  selected: boolean
  onClick: () => void
}

const classificationConfig = {
  'Strong Trend': { color: 'var(--accent-green)', bg: 'rgba(74,222,128,0.08)', border: 'rgba(74,222,128,0.3)' },
  'Early Trend': { color: 'var(--accent-gold)', bg: 'rgba(245,158,11,0.08)', border: 'rgba(245,158,11,0.3)' },
  'Fad': { color: 'var(--accent-red)', bg: 'rgba(248,113,113,0.08)', border: 'rgba(248,113,113,0.3)' },
}

export default function TrendCard({ trend, index, selected, onClick }: Props) {
  const config = classificationConfig[trend.classification]
  
  return (
    <div
      onClick={onClick}
      className="border rounded-xl p-5 cursor-pointer transition-all duration-300"
      style={{
        borderColor: selected ? config.border : 'var(--border-moss)',
        backgroundColor: selected ? config.bg : 'var(--bg-card)',
        animation: `cardReveal 0.5s ease forwards`,
        animationDelay: `${index * 0.1}s`,
        opacity: 0,
        boxShadow: selected ? `0 0 20px ${config.color}20` : 'none',
      }}
    >
      {/* Top row */}
      <div className="flex items-start justify-between mb-3">
        <div className="flex-1">
          <span className="font-mono text-[10px] tracking-widest uppercase"
            style={{ color: config.color }}>
            {trend.classification}
          </span>
          <h3 className="font-display text-lg text-[var(--text-primary)] mt-0.5 leading-tight">
            {trend.name}
          </h3>
        </div>
        {/* Score circle */}
        <div className="flex-shrink-0 ml-3">
          <div className="w-12 h-12 rounded-full border-2 flex items-center justify-center font-mono text-sm font-bold"
            style={{ borderColor: config.color, color: config.color, backgroundColor: config.bg }}>
            {trend.score}
          </div>
        </div>
      </div>

      {/* Score bar */}
      <div className="w-full h-0.5 bg-[var(--bg-deep)] rounded-full mb-3 overflow-hidden">
        <div className="h-full rounded-full score-bar"
          style={{ width: `${trend.score}%`, backgroundColor: config.color }} />
      </div>

      {/* Brief */}
      <p className="text-xs text-[var(--text-muted)] leading-relaxed mb-3 line-clamp-2">
        {trend.opportunityBrief}
      </p>

      {/* Bottom meta */}
      <div className="grid grid-cols-2 gap-2 text-xs font-mono">
        <div className="bg-[var(--bg-deep)]/60 rounded-lg p-2">
          <span className="text-[var(--text-dim)] block text-[10px] uppercase tracking-wider mb-0.5">Product</span>
          <span className="text-[var(--text-muted)] line-clamp-1">{trend.productConcept}</span>
        </div>
        <div className="bg-[var(--bg-deep)]/60 rounded-lg p-2">
          <span className="text-[var(--text-dim)] block text-[10px] uppercase tracking-wider mb-0.5">Launch</span>
          <span className="text-[var(--text-muted)]">{trend.launchTiming}</span>
        </div>
      </div>
    </div>
  )
}

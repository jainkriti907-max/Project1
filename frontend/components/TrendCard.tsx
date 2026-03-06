import { useState } from 'react'
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

function SignalBar({ label, value, color }: { label: string; value: number; color: string }) {
  return (
    <div className="mb-2">
      <div className="flex justify-between items-center mb-1">
        <span className="font-mono text-[10px] text-[var(--text-dim)] uppercase tracking-wider">{label}</span>
        <span className="font-mono text-[10px]" style={{ color }}>{value}/100</span>
      </div>
      <div className="w-full h-1 bg-[var(--bg-deep)] rounded-full overflow-hidden">
        <div className="h-full rounded-full transition-all duration-700"
          style={{ width: `${value}%`, backgroundColor: color }} />
      </div>
    </div>
  )
}

function DataPill({ label, value }: { label: string; value: string | number }) {
  return (
    <div className="bg-[var(--bg-deep)]/80 rounded-lg p-2.5 border border-[var(--border-moss)]">
      <span className="font-mono text-[9px] text-[var(--text-dim)] uppercase tracking-wider block mb-0.5">{label}</span>
      <span className="font-mono text-xs text-[var(--text-primary)]">{value}</span>
    </div>
  )
}

export default function TrendCard({ trend, index, selected, onClick }: Props) {
  const [expanded, setExpanded] = useState(false)
  const config = classificationConfig[trend.classification]
  const dp = (trend as any).dataPoints

  const handleMoreDetails = (e: React.MouseEvent) => {
    e.stopPropagation()
    setExpanded(prev => !prev)
  }

  return (
    <div
      className="border rounded-xl transition-all duration-300"
      style={{
        borderColor: selected || expanded ? config.border : 'var(--border-moss)',
        backgroundColor: selected ? config.bg : 'var(--bg-card)',
        animation: 'cardReveal 0.5s ease forwards',
        animationDelay: `${index * 0.1}s`,
        opacity: 0,
        boxShadow: selected || expanded ? `0 0 24px ${config.color}18` : 'none',
      }}
    >
      {/* Main card */}
      <div className="p-5 cursor-pointer" onClick={onClick}>
        <div className="flex items-start justify-between mb-3">
          <div className="flex-1">
            <span className="font-mono text-[10px] tracking-widest uppercase" style={{ color: config.color }}>
              {trend.classification}
            </span>
            <h3 className="font-display text-lg text-[var(--text-primary)] mt-0.5 leading-tight">
              {trend.name}
            </h3>
          </div>
          <div className="flex-shrink-0 ml-3">
            <div className="w-12 h-12 rounded-full border-2 flex items-center justify-center font-mono text-sm font-bold"
              style={{ borderColor: config.color, color: config.color, backgroundColor: config.bg }}>
              {trend.score}
            </div>
          </div>
        </div>

        <div className="w-full h-0.5 bg-[var(--bg-deep)] rounded-full mb-3 overflow-hidden">
          <div className="h-full rounded-full score-bar"
            style={{ width: `${trend.score}%`, backgroundColor: config.color }} />
        </div>

        <p className="text-xs text-[var(--text-muted)] leading-relaxed mb-3 line-clamp-2">
          {trend.opportunityBrief}
        </p>

        <div className="grid grid-cols-2 gap-2 text-xs font-mono mb-3">
          <div className="bg-[var(--bg-deep)]/60 rounded-lg p-2">
            <span className="text-[var(--text-dim)] block text-[10px] uppercase tracking-wider mb-0.5">Product</span>
            <span className="text-[var(--text-muted)] line-clamp-1">{trend.productConcept}</span>
          </div>
          <div className="bg-[var(--bg-deep)]/60 rounded-lg p-2">
            <span className="text-[var(--text-dim)] block text-[10px] uppercase tracking-wider mb-0.5">Launch</span>
            <span className="text-[var(--text-muted)]">{trend.launchTiming}</span>
          </div>
        </div>

        <div className="flex justify-end">
          <button
            onClick={handleMoreDetails}
            className="flex items-center gap-1.5 font-mono text-[10px] tracking-widest uppercase px-3 py-1.5 rounded-full border transition-all duration-200"
            style={{
              borderColor: expanded ? config.color : 'var(--border-moss-bright)',
              color: expanded ? config.color : 'var(--text-muted)',
              backgroundColor: expanded ? config.bg : 'transparent',
            }}
          >
            {expanded ? 'Hide Details' : 'More Details'}
            <svg width="10" height="10" viewBox="0 0 10 10" fill="none"
              style={{ transform: expanded ? 'rotate(180deg)' : 'rotate(0deg)', transition: 'transform 0.3s ease' }}>
              <path d="M2 3.5L5 6.5L8 3.5" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
          </button>
        </div>
      </div>

      {/* Expanded panel */}
      {expanded && (
        <div className="px-5 pb-5 border-t" style={{ borderColor: 'var(--border-moss)' }}>
          <div className="pt-4 space-y-5">

            <div>
              <p className="font-mono text-[10px] text-[var(--accent-green)] tracking-widest uppercase mb-2">📋 Opportunity Brief</p>
              <p className="text-xs text-[var(--text-muted)] leading-relaxed">{trend.opportunityBrief}</p>
            </div>

            <div>
              <p className="font-mono text-[10px] text-[var(--accent-green)] tracking-widest uppercase mb-3">📡 Signal Breakdown</p>
              <SignalBar label="Search Velocity" value={trend.signals.velocity} color="var(--accent-green)" />
              <SignalBar label="Consumer Buzz" value={trend.signals.consumerBuzz} color="var(--accent-gold)" />
              <SignalBar label="Market Potential" value={trend.signals.marketPotential} color="var(--accent-blue)" />
              <SignalBar label="Scientific Backing" value={trend.signals.scientificBacking} color="#a78bfa" />
              <SignalBar label="Low Competition" value={100 - trend.signals.competition} color="var(--accent-green)" />
            </div>

            {dp && (
              <>
                {dp.googleTrends && (
                  <div>
                    <p className="font-mono text-[10px] text-[var(--accent-green)] tracking-widest uppercase mb-2">🔍 Google Trends (India)</p>
                    <div className="grid grid-cols-2 gap-2">
                      <DataPill label="YoY Growth" value={dp.googleTrends.yoyGrowth} />
                      <DataPill label="Peak Month" value={dp.googleTrends.peakMonth} />
                      <DataPill label="Velocity Score" value={`${dp.googleTrends.velocityScore}/100`} />
                      <DataPill label="Direction" value={dp.googleTrends.trendDirection} />
                    </div>
                  </div>
                )}

                {dp.reddit && (
                  <div>
                    <p className="font-mono text-[10px] text-[var(--accent-green)] tracking-widest uppercase mb-2">💬 Reddit Community</p>
                    <div className="grid grid-cols-2 gap-2 mb-2">
                      <DataPill label="Posts (90 days)" value={dp.reddit.postCount.toLocaleString()} />
                      <DataPill label="Avg Upvotes" value={dp.reddit.avgUpvotes.toLocaleString()} />
                      <DataPill label="Sentiment" value={`${dp.reddit.sentimentScore}% positive`} />
                    </div>
                    {dp.reddit.topThemes?.length > 0 && (
                      <div className="flex flex-wrap gap-1 mt-1">
                        {dp.reddit.topThemes.map((theme: string) => (
                          <span key={theme} className="font-mono text-[9px] px-2 py-0.5 rounded-full border"
                            style={{ borderColor: 'var(--border-moss)', color: 'var(--text-dim)' }}>
                            {theme}
                          </span>
                        ))}
                      </div>
                    )}
                  </div>
                )}

                {dp.pubmed && (
                  <div>
                    <p className="font-mono text-[10px] text-[var(--accent-green)] tracking-widest uppercase mb-2">🔬 PubMed Research (2022-2025)</p>
                    <div className="grid grid-cols-2 gap-2">
                      <DataPill label="Published Papers" value={dp.pubmed.paperCount.toLocaleString()} />
                      <DataPill label="Clinical Trials" value={dp.pubmed.clinicalTrials} />
                      <DataPill label="Evidence Quality" value={dp.pubmed.evidenceQuality} />
                      <DataPill label="Research Momentum" value={dp.pubmed.researchMomentum} />
                    </div>
                  </div>
                )}

                {dp.ecommerce && (
                  <div>
                    <p className="font-mono text-[10px] text-[var(--accent-green)] tracking-widest uppercase mb-2">🛒 Ecommerce (Amazon.in + Nykaa)</p>
                    <div className="grid grid-cols-2 gap-2 mb-2">
                      <DataPill label="Avg Rating" value={`${dp.ecommerce.avgRating} ⭐`} />
                      <DataPill label="Total Reviews" value={dp.ecommerce.reviewCount.toLocaleString()} />
                      <DataPill label="YoY Sales Growth" value={dp.ecommerce.yoySalesGrowth} />
                    </div>
                    <div className="bg-[var(--bg-deep)]/80 rounded-lg p-3 border border-[var(--border-moss)]">
                      <span className="font-mono text-[9px] text-[var(--accent-green)] uppercase tracking-wider block mb-1">💡 Market Gap Identified</span>
                      <span className="font-mono text-xs text-[var(--text-primary)]">{dp.ecommerce.marketGap}</span>
                    </div>
                  </div>
                )}

                {dp.youtube && (
                  <div>
                    <p className="font-mono text-[10px] text-[var(--accent-green)] tracking-widest uppercase mb-2">🎥 YouTube India</p>
                    <div className="grid grid-cols-3 gap-2">
                      <DataPill label="Views (90d)" value={`${dp.youtube.viewCountMillions}M`} />
                      <DataPill label="Creators" value={dp.youtube.creatorAdoption} />
                      <DataPill label="Trend Score" value={`${dp.youtube.trendingScore}/100`} />
                    </div>
                  </div>
                )}
              </>
            )}

            <div>
              <p className="font-mono text-[10px] text-[var(--accent-green)] tracking-widest uppercase mb-2">📦 Product Recommendation</p>
              <div className="space-y-2">
                <div className="bg-[var(--bg-deep)]/80 rounded-lg p-3 border border-[var(--border-moss)]">
                  <span className="font-mono text-[9px] text-[var(--text-dim)] uppercase tracking-wider block mb-1">Concept</span>
                  <span className="font-mono text-xs text-[var(--text-primary)]">{trend.productConcept}</span>
                </div>
                <div className="bg-[var(--bg-deep)]/80 rounded-lg p-3 border border-[var(--border-moss)]">
                  <span className="font-mono text-[9px] text-[var(--text-dim)] uppercase tracking-wider block mb-1">Packaging Format</span>
                  <span className="font-mono text-xs text-[var(--text-primary)]">{trend.packagingFormat}</span>
                </div>
                <div className="grid grid-cols-2 gap-2">
                  <div className="bg-[var(--bg-deep)]/80 rounded-lg p-3 border border-[var(--border-moss)]">
                    <span className="font-mono text-[9px] text-[var(--text-dim)] uppercase tracking-wider block mb-1">Market Size</span>
                    <span className="font-mono text-xs" style={{ color: config.color }}>{trend.marketOpportunity}</span>
                  </div>
                  <div className="bg-[var(--bg-deep)]/80 rounded-lg p-3 border border-[var(--border-moss)]">
                    <span className="font-mono text-[9px] text-[var(--text-dim)] uppercase tracking-wider block mb-1">Launch Window</span>
                    <span className="font-mono text-xs text-[var(--text-primary)]">{trend.launchTiming}</span>
                  </div>
                </div>
              </div>
            </div>

          </div>
        </div>
      )}
    </div>
  )
}

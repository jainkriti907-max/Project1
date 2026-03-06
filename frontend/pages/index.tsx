import { useState, useCallback } from 'react'
import Head from 'next/head'
import RadarChart from '../components/RadarChart'
import TrendCard from '../components/TrendCard'
import ScanButton from '../components/ScanButton'
import StatusLog from '../components/StatusLog'

export interface Trend {
  name: string
  score: number
  classification: 'Strong Trend' | 'Early Trend' | 'Fad'
  marketOpportunity: string
  productConcept: string
  packagingFormat: string
  launchTiming: string
  opportunityBrief: string
  signals: {
    velocity: number
    marketPotential: number
    scientificBacking: number
    consumerBuzz: number
    competition: number
  }
}

type ScanState = 'idle' | 'scanning' | 'done' | 'error'

const LOG_STEPS = [
  { msg: '⚡ Initializing Mosaic Radar Engine...', delay: 0 },
  { msg: '🔍 Querying Google Trends API...', delay: 600 },
  { msg: '📡 Scanning Reddit wellness communities...', delay: 1200 },
  { msg: '🎥 Parsing YouTube wellness content...', delay: 1800 },
  { msg: '🔬 Searching PubMed research publications...', delay: 2400 },
  { msg: '🛒 Analysing ecommerce reviews (Amazon/Nykaa)...', delay: 3000 },
  { msg: '🧠 Scoring trends: velocity · market · science · buzz...', delay: 3600 },
  { msg: '✅ Aggregating opportunity briefs...', delay: 4200 },
]

export default function Home() {
  const [scanState, setScanState] = useState<ScanState>('idle')
  const [trends, setTrends] = useState<Trend[]>([])
  const [logs, setLogs] = useState<string[]>([])
  const [selectedTrend, setSelectedTrend] = useState<Trend | null>(null)
  const [error, setError] = useState<string | null>(null)

  const runScan = useCallback(async () => {
    setScanState('scanning')
    setTrends([])
    setLogs([])
    setError(null)
    setSelectedTrend(null)

    // Stream logs with delays
    LOG_STEPS.forEach(({ msg, delay }) => {
      setTimeout(() => setLogs(prev => [...prev, msg]), delay)
    })

    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000'
      const res = await fetch(`${apiUrl}/scan`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ category: 'wellness', region: 'IN' }),
      })

      if (!res.ok) throw new Error(`API error: ${res.status}`)

      const data = await res.json()
      
      setTimeout(() => {
        setTrends(data.trends || [])
        setScanState('done')
        if (data.trends?.length > 0) setSelectedTrend(data.trends[0])
      }, 4800)

    } catch (err: unknown) {
      const message = err instanceof Error ? err.message : 'Unknown error'
      setTimeout(() => {
        setLogs(prev => [...prev, `❌ Error: ${message}`])
        setError(message)
        setScanState('error')
      }, 4800)
    }
  }, [])

  return (
    <>
      <Head>
        <title>Mosaic Trends Radar — Wellness Intelligence</title>
        <meta name="description" content="Real-time wellness trend detection for Mosaic Wellness founders" />
        <link rel="icon" href="/favicon.svg" />
      </Head>

      <div className="grid-bg noise min-h-screen">
        {/* Header */}
        <header className="border-b border-[var(--border-moss)] bg-[var(--bg-deep)]/80 backdrop-blur-sm sticky top-0 z-50">
          <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-8 h-8 relative">
                <svg viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <circle cx="16" cy="16" r="14" stroke="#4ade80" strokeWidth="1" opacity="0.4"/>
                  <circle cx="16" cy="16" r="9" stroke="#4ade80" strokeWidth="1" opacity="0.5"/>
                  <circle cx="16" cy="16" r="4" stroke="#4ade80" strokeWidth="1" opacity="0.6"/>
                  <circle cx="16" cy="16" r="1.5" fill="#4ade80"/>
                  <line x1="16" y1="2" x2="16" y2="30" stroke="#4ade80" strokeWidth="0.5" opacity="0.2"/>
                  <line x1="2" y1="16" x2="30" y2="16" stroke="#4ade80" strokeWidth="0.5" opacity="0.2"/>
                </svg>
              </div>
              <div>
                <h1 className="font-display text-xl text-[var(--text-primary)] leading-none">
                  Mosaic Trends Radar
                </h1>
                <p className="font-mono text-[10px] text-[var(--text-muted)] tracking-widest uppercase mt-0.5">
                  Wellness Intelligence Engine
                </p>
              </div>
            </div>
            <div className="flex items-center gap-6">
              <div className="hidden md:flex items-center gap-4 font-mono text-xs text-[var(--text-dim)]">
                <span>Sources: Google · Reddit · YouTube · PubMed · Ecomm</span>
              </div>
              <div className={`flex items-center gap-2 font-mono text-xs px-3 py-1.5 rounded-full border ${
                scanState === 'scanning' 
                  ? 'border-[var(--accent-green)]/40 text-[var(--accent-green)] bg-[var(--accent-green)]/5' 
                  : scanState === 'done'
                  ? 'border-[var(--accent-green)]/30 text-[var(--accent-green)]/70 bg-[var(--accent-green)]/5'
                  : 'border-[var(--border-moss)] text-[var(--text-dim)]'
              }`}>
                <span className={`w-1.5 h-1.5 rounded-full ${
                  scanState === 'scanning' ? 'bg-[var(--accent-green)] animate-pulse' : 
                  scanState === 'done' ? 'bg-[var(--accent-green)]/60' : 'bg-[var(--text-dim)]'
                }`}/>
                {scanState === 'idle' ? 'STANDBY' : scanState === 'scanning' ? 'SCANNING' : scanState === 'done' ? `${trends.length} TRENDS FOUND` : 'ERROR'}
              </div>
            </div>
          </div>
        </header>

        <main className="max-w-7xl mx-auto px-6 py-8">
          
          {/* Hero scan section */}
          <div className="flex flex-col lg:flex-row gap-8 mb-10">
            {/* Radar visual + scan button */}
            <div className="lg:w-80 flex flex-col items-center gap-6">
              <div className="relative w-64 h-64">
                {/* Radar rings */}
                {[0, 1, 2, 3].map(i => (
                  <div key={i} className="absolute inset-0 rounded-full border border-[var(--accent-green)]/10 m-auto"
                    style={{ width: `${100 - i * 20}%`, height: `${100 - i * 20}%`, top: '50%', left: '50%', transform: 'translate(-50%, -50%)' }}
                  />
                ))}
                {/* Cross hairs */}
                <div className="absolute inset-0 flex items-center justify-center">
                  <div className="w-full h-px bg-[var(--accent-green)]/10"/>
                </div>
                <div className="absolute inset-0 flex items-center justify-center">
                  <div className="h-full w-px bg-[var(--accent-green)]/10"/>
                </div>
                {/* Sweep line */}
                {scanState === 'scanning' && (
                  <div className="absolute inset-0 radar-sweep">
                    <div className="absolute top-1/2 left-1/2 w-1/2 h-px origin-left"
                      style={{ background: 'linear-gradient(90deg, rgba(74,222,128,0.8), transparent)' }}
                    />
                    <div className="absolute top-1/2 left-1/2 w-full h-full origin-top-left rounded-br-full rounded-tr-full"
                      style={{ background: 'conic-gradient(from 0deg, rgba(74,222,128,0.12), transparent 60deg)', transform: 'translate(-50%, -50%)' }}
                    />
                  </div>
                )}
                {/* Blips when done */}
                {scanState === 'done' && trends.slice(0, 7).map((t, i) => {
                  const angle = (i / 7) * Math.PI * 2
                  const r = 30 + (t.score / 100) * 70
                  const x = 50 + r * Math.cos(angle) * 0.45
                  const y = 50 + r * Math.sin(angle) * 0.45
                  return (
                    <div key={i}
                      className="absolute w-2 h-2 rounded-full cursor-pointer"
                      style={{
                        left: `${x}%`, top: `${y}%`,
                        transform: 'translate(-50%, -50%)',
                        backgroundColor: t.score > 75 ? 'var(--accent-green)' : t.score > 55 ? 'var(--accent-gold)' : 'var(--accent-red)',
                        boxShadow: `0 0 6px currentColor`,
                        animation: `blip 2s ease-in-out ${i * 0.3}s infinite`
                      }}
                      onClick={() => setSelectedTrend(t)}
                      title={t.name}
                    />
                  )
                })}
                {/* Center dot */}
                <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-3 h-3 rounded-full bg-[var(--accent-green)] glow-pulse"/>
              </div>

              <ScanButton state={scanState} onScan={runScan} />

              <p className="text-center font-mono text-xs text-[var(--text-dim)] leading-relaxed max-w-xs">
                Scans live signals across 5 data sources to surface emerging wellness opportunities
              </p>
            </div>

            {/* Right: Logs + Radar chart */}
            <div className="flex-1 flex flex-col gap-6">
              {scanState !== 'idle' && (
                <StatusLog logs={logs} state={scanState} />
              )}
              {scanState === 'idle' && (
                <div className="flex-1 border border-[var(--border-moss)] rounded-xl p-8 flex flex-col justify-center items-start bg-[var(--bg-card)]/40">
                  <p className="font-mono text-xs text-[var(--accent-green)] tracking-widest uppercase mb-3">Ready to scan</p>
                  <h2 className="font-display text-3xl text-[var(--text-primary)] mb-4 leading-tight">
                    Discover what wellness<br/>consumers want next.
                  </h2>
                  <p className="text-[var(--text-muted)] text-sm leading-relaxed max-w-lg">
                    The Mosaic Trends Radar aggregates signals from Google Trends, Reddit, YouTube, PubMed, and ecommerce reviews to identify emerging wellness trends — before they go mainstream.
                  </p>
                  <div className="mt-6 flex flex-wrap gap-2">
                    {['Adaptogens', 'Longevity', 'Gut Health', 'Nootropics', 'Sleep Science'].map(tag => (
                      <span key={tag} className="font-mono text-xs px-2 py-1 rounded border border-[var(--border-moss)] text-[var(--text-dim)]">
                        {tag}
                      </span>
                    ))}
                  </div>
                </div>
              )}
              {scanState === 'done' && selectedTrend && (
                <div className="border border-[var(--border-moss)] rounded-xl p-6 bg-[var(--bg-card)]/40">
                  <p className="font-mono text-xs text-[var(--accent-green)] tracking-widest uppercase mb-2">Selected Signal</p>
                  <h3 className="font-display text-2xl text-[var(--text-primary)] mb-3">{selectedTrend.name}</h3>
                  <p className="text-sm text-[var(--text-muted)] leading-relaxed">{selectedTrend.opportunityBrief}</p>
                  <div className="mt-4 grid grid-cols-2 gap-3 text-xs font-mono">
                    <div>
                      <span className="text-[var(--text-dim)] block mb-1">Market Opportunity</span>
                      <span className="text-[var(--text-primary)]">{selectedTrend.marketOpportunity}</span>
                    </div>
                    <div>
                      <span className="text-[var(--text-dim)] block mb-1">Launch Timing</span>
                      <span className="text-[var(--text-primary)]">{selectedTrend.launchTiming}</span>
                    </div>
                  </div>
                  <RadarChart signals={selectedTrend.signals} />
                </div>
              )}
            </div>
          </div>

          {/* Trend Cards Grid */}
          {scanState === 'done' && trends.length > 0 && (
            <div>
              <div className="flex items-center gap-3 mb-6">
                <div className="h-px flex-1 bg-[var(--border-moss)]"/>
                <p className="font-mono text-xs text-[var(--text-muted)] tracking-widest uppercase">
                  {trends.length} Opportunity Signals Detected
                </p>
                <div className="h-px flex-1 bg-[var(--border-moss)]"/>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {trends.map((trend, i) => (
                  <TrendCard
                    key={trend.name}
                    trend={trend}
                    index={i}
                    selected={selectedTrend?.name === trend.name}
                    onClick={() => setSelectedTrend(trend)}
                  />
                ))}
              </div>
            </div>
          )}

          {scanState === 'error' && (
            <div className="border border-red-900/40 bg-red-950/20 rounded-xl p-6 text-center">
              <p className="font-mono text-xs text-red-400 mb-2 tracking-widest uppercase">Scan Failed</p>
              <p className="text-sm text-red-300/70">{error}</p>
              <p className="text-xs text-[var(--text-dim)] mt-2">Check that the backend is running at {process.env.NEXT_PUBLIC_API_URL}</p>
            </div>
          )}
        </main>

        <footer className="border-t border-[var(--border-moss)] mt-16 py-6">
          <div className="max-w-7xl mx-auto px-6 flex items-center justify-between">
            <p className="font-mono text-xs text-[var(--text-dim)]">Mosaic Trends Radar · Fellowship Builder Challenge 2025</p>
            <p className="font-mono text-xs text-[var(--text-dim)]">Powered by live signals · Flask + Next.js</p>
          </div>
        </footer>
      </div>
    </>
  )
}

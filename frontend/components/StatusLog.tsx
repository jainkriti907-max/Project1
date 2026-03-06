interface Props {
  logs: string[]
  state: 'scanning' | 'done' | 'error' | 'idle'
}

export default function StatusLog({ logs, state }: Props) {
  return (
    <div className="border border-[var(--border-moss)] rounded-xl bg-[var(--bg-card)]/60 p-4 font-mono text-xs">
      <div className="flex items-center gap-2 mb-3 pb-3 border-b border-[var(--border-moss)]">
        <div className={`w-2 h-2 rounded-full ${state === 'scanning' ? 'bg-[var(--accent-green)] animate-pulse' : state === 'done' ? 'bg-[var(--accent-green)]' : 'bg-red-400'}`}/>
        <span className="text-[var(--text-muted)] tracking-widest uppercase text-[10px]">
          Radar Engine Log
        </span>
      </div>
      <div className="space-y-1.5 max-h-48 overflow-y-auto">
        {logs.map((log, i) => (
          <p key={i} className={`leading-relaxed ${
            log.startsWith('❌') ? 'text-red-400' : 
            log.startsWith('✅') ? 'text-[var(--accent-green)]' : 
            'text-[var(--text-muted)]'
          }`} style={{ animation: `cardReveal 0.3s ease forwards`, animationDelay: `${i * 0.05}s`, opacity: 0 }}>
            <span className="text-[var(--text-dim)] mr-2">[{String(i + 1).padStart(2, '0')}]</span>
            {log}
          </p>
        ))}
        {state === 'scanning' && (
          <p className="text-[var(--text-dim)] flex items-center gap-1">
            <span className="animate-pulse">▋</span>
          </p>
        )}
      </div>
    </div>
  )
}

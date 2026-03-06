interface Props {
  state: 'idle' | 'scanning' | 'done' | 'error'
  onScan: () => void
}

export default function ScanButton({ state, onScan }: Props) {
  const isScanning = state === 'scanning'
  const isDone = state === 'done'

  return (
    <button
      onClick={onScan}
      disabled={isScanning}
      className={`relative w-48 py-3 px-6 rounded-full font-mono text-sm tracking-widest uppercase transition-all duration-300
        ${isScanning
          ? 'border border-[var(--accent-green)]/40 text-[var(--accent-green)] cursor-not-allowed bg-[var(--accent-green)]/5'
          : isDone
          ? 'border border-[var(--accent-green)]/50 text-[var(--text-primary)] bg-[var(--bg-card)] hover:bg-[var(--bg-card-hover)] hover:border-[var(--accent-green)]/70'
          : 'border border-[var(--accent-green)] text-[var(--bg-deep)] bg-[var(--accent-green)] hover:bg-[var(--accent-green)]/90 shadow-[0_0_30px_rgba(74,222,128,0.3)]'
        }`}
    >
      {isScanning ? (
        <span className="flex items-center justify-center gap-2">
          <span className="w-3 h-3 border border-[var(--accent-green)] border-t-transparent rounded-full animate-spin"/>
          Scanning...
        </span>
      ) : isDone ? (
        'Rescan'
      ) : (
        'Run Radar Scan'
      )}
    </button>
  )
}

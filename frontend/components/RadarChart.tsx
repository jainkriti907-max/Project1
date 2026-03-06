import { Radar, RadarChart as RechartsRadar, PolarGrid, PolarAngleAxis, ResponsiveContainer } from 'recharts'

interface Signals {
  velocity: number
  marketPotential: number
  scientificBacking: number
  consumerBuzz: number
  competition: number
}

interface Props {
  signals: Signals
}

export default function RadarChart({ signals }: Props) {
  const data = [
    { subject: 'Velocity', value: signals.velocity },
    { subject: 'Market', value: signals.marketPotential },
    { subject: 'Science', value: signals.scientificBacking },
    { subject: 'Buzz', value: signals.consumerBuzz },
    { subject: 'Competition', value: 100 - signals.competition }, // invert: lower competition is better
  ]

  return (
    <div className="mt-4 h-40">
      <ResponsiveContainer width="100%" height="100%">
        <RechartsRadar data={data} margin={{ top: 4, right: 20, bottom: 4, left: 20 }}>
          <PolarGrid stroke="rgba(74,222,128,0.12)" />
          <PolarAngleAxis
            dataKey="subject"
            tick={{ fill: 'var(--text-dim)', fontSize: 10, fontFamily: 'var(--font-mono)' }}
          />
          <Radar
            name="Signal"
            dataKey="value"
            stroke="rgba(74,222,128,0.8)"
            fill="rgba(74,222,128,0.12)"
            strokeWidth={1.5}
          />
        </RechartsRadar>
      </ResponsiveContainer>
    </div>
  )
}

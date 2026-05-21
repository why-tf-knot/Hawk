import type { TimeSeriesPoint } from '../types'

interface Props {
  points: TimeSeriesPoint[]
  availableYears?: number[]
  note?: string
}

export function TrendCharts({ points, availableYears = [], note }: Props) {
  if (!points.length) {
    return <div className="charts">No time-series data yet.</div>
  }

  const maxValue = Math.max(...points.map((point) => point.value))

  return (
    <div className="charts" aria-label="Trend charts">
      <h2>Trend charts</h2>
      {availableYears.length ? (
        <p className="muted">Temporal coverage: {availableYears[0]}–{availableYears[availableYears.length - 1]}</p>
      ) : null}
      <svg viewBox="0 0 300 120" role="img" aria-label="Atmospheric anomaly trend">
        {points.map((point, index) => {
          const x = (index / Math.max(points.length - 1, 1)) * 280 + 10
          const y = 100 - (point.value / maxValue) * 80
          return <circle key={point.date} cx={x} cy={y} r={3} fill="#0ea5e9" />
        })}
      </svg>
      <p className="muted">{note ?? 'Uncertainty-aware trend support only; raw values remain available by date.'}</p>
    </div>
  )
}

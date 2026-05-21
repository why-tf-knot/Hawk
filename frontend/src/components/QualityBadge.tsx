import type { ConfidenceLevel } from '../types'

interface Props {
  confidence: ConfidenceLevel
  score: number
}

export function QualityBadge({ confidence, score }: Props) {
  return <span className={`badge badge-${confidence}`}>{confidence} ({Math.round(score * 100)}%)</span>
}

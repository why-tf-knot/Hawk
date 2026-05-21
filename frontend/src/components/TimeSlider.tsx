interface Props {
  value: number
  onChange: (value: number) => void
  max?: number
}

export function TimeSlider({ value, onChange, max = 12 }: Props) {
  return (
    <section className="timeslider" aria-label="Time slider">
      <h2>Time slider</h2>
      <input type="range" min={0} max={max} value={value} onChange={(e) => onChange(Number(e.target.value))} />
      <span>Frame: {value}</span>
    </section>
  )
}

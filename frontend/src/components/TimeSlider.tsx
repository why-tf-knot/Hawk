interface Props {
  value: number
  onChange: (value: number) => void
}

export function TimeSlider({ value, onChange }: Props) {
  return (
    <section className="timeslider" aria-label="Time slider">
      <h2>Time slider</h2>
      <input type="range" min={0} max={12} value={value} onChange={(e) => onChange(Number(e.target.value))} />
      <span>Frame: {value}</span>
    </section>
  )
}

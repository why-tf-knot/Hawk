import type { LayerMetadata } from '../types'

interface Props {
  layers: LayerMetadata[]
}

export function MapLegend({ layers }: Props) {
  return (
    <section className="legend" aria-label="Map legend">
      <h2>Map legend</h2>
      <p className="muted">Atmospheric layers are coarse-scale and shown with uncertainty-aware interpretation.</p>
      {layers.map((layer) => (
        <div key={layer.layer_name} className="legend-row">
          <strong>{layer.title}</strong>
          <span>{layer.native_resolution_m}m</span>
        </div>
      ))}
    </section>
  )
}

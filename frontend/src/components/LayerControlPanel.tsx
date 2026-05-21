import type { LayerMetadata } from '../types'

interface Props {
  layers: LayerMetadata[]
  enabledLayers: Record<string, boolean>
  onToggle: (layerName: string) => void
}

export function LayerControlPanel({ layers, enabledLayers, onToggle }: Props) {
  return (
    <section className="panel-section">
      <h2>Layer control panel</h2>
      <ul className="layer-list">
        {layers.map((layer) => (
          <li key={layer.layer_name}>
            <label title={layer.scale_warning}>
              <input
                type="checkbox"
                checked={Boolean(enabledLayers[layer.layer_name])}
                onChange={() => onToggle(layer.layer_name)}
              />
              {layer.title}
            </label>
          </li>
        ))}
      </ul>
    </section>
  )
}

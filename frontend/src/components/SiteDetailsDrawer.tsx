import type { IndustrialPolygon, TimeSeriesPoint } from '../types'

interface Props {
  site?: IndustrialPolygon
  timeseries: TimeSeriesPoint[]
}

export function SiteDetailsDrawer({ site, timeseries }: Props) {
  if (!site) {
    return <aside className="drawer">Select an industrial zone to view details.</aside>
  }

  return (
    <aside className="drawer">
      <h2>Site details drawer</h2>
      <p><strong>Site ID:</strong> {site.site_id}</p>
      <p><strong>Area:</strong> {site.metrics.area_sq_km.toFixed(2)} km²</p>
      <p><strong>Class:</strong> {site.class_name}</p>
      <p><strong>Observation completeness:</strong> {Math.round(site.metrics.completeness * 100)}%</p>
      <p className="warning">
        Atmospheric attribution is probabilistic and coarse-scale; avoid rooftop-level interpretation.
      </p>
      <details>
        <summary>Data quality / confidence badges</summary>
        <ul>
          <li>Native resolution: {site.quality.source_resolution_m}m</li>
          <li>Masking fraction: {Math.round(site.quality.masking_fraction * 100)}%</li>
          <li>Valid observations: {site.quality.valid_observations}</li>
        </ul>
      </details>
      <p><strong>Points in trend:</strong> {timeseries.length}</p>
    </aside>
  )
}

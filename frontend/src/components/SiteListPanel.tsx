import type { IndustrialPolygon } from '../types'
import { QualityBadge } from './QualityBadge'

interface Props {
  sites: IndustrialPolygon[]
  onSelect: (siteId: string) => void
}

export function SiteListPanel({ sites, onSelect }: Props) {
  return (
    <section className="panel-section">
      <h2>Site list panel</h2>
      <ul className="site-list">
        {sites.map((site) => (
          <li key={site.site_id}>
            <button type="button" onClick={() => onSelect(site.site_id)}>
              {site.site_id}
            </button>
            <QualityBadge confidence={site.confidence} score={site.confidence_score} />
          </li>
        ))}
      </ul>
    </section>
  )
}

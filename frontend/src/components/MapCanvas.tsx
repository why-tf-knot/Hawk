import { GeoJSON, MapContainer, TileLayer } from 'react-leaflet'
import type { GeoJsonObject } from 'geojson'
import type { CityAOI, IndustrialPolygon } from '../types'

interface Props {
  city?: CityAOI
  polygons: IndustrialPolygon[]
  selectedSiteId?: string
  onSelectSite: (siteId: string) => void
}

export function MapCanvas({ city, polygons, selectedSiteId, onSelectSite }: Props) {
  const center = city?.center ?? [20, 0]
  const zoom = city ? 11 : 2

  return (
    <div className="map-canvas" role="region" aria-label="Leaflet map canvas">
      <MapContainer center={center} zoom={zoom} className="leaflet-root">
        <TileLayer
          attribution='&copy; OpenStreetMap contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        {city ? <GeoJSON data={city.geojson as GeoJsonObject} style={{ color: '#2563eb', weight: 2 }} /> : null}
        {polygons.map((polygon) => (
          <GeoJSON
            key={polygon.site_id}
            data={polygon.geometry as GeoJsonObject}
            style={{ color: polygon.site_id === selectedSiteId ? '#f97316' : '#dc2626', weight: 2 }}
            eventHandlers={{ click: () => onSelectSite(polygon.site_id) }}
          />
        ))}
      </MapContainer>
    </div>
  )
}

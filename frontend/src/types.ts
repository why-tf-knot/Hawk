import type { Geometry } from 'geojson'

export type ConfidenceLevel = 'low' | 'medium' | 'high'

export interface CityAOI {
  id: string
  name: string
  country: string
  center: [number, number]
  bbox: [number, number, number, number]
  geojson: Geometry
}

export interface QualityMetadata {
  source_resolution_m: number
  masking_fraction: number
  valid_observations: number
  qa_notes: string[]
}

export interface LayerMetadata {
  layer_name: string
  title: string
  unit?: string | null
  native_resolution_m: number
  scale_warning: string
  quality: QualityMetadata
}

export interface SiteMetrics {
  site_id: string
  area_sq_km: number
  industrial_score: number
  thermal_anomaly_index?: number | null
  completeness: number
}

export interface IndustrialPolygon {
  site_id: string
  city_id: string
  class_name: string
  confidence: ConfidenceLevel
  confidence_score: number
  geometry: Geometry
  metrics: SiteMetrics
  quality: QualityMetadata
}

export interface AtmosphericZone {
  zone_id: string
  site_id: string
  zone_type: string
  geometry: Geometry
  quality: QualityMetadata
}

export interface TimeSeriesPoint {
  date: string
  value: number
  metric: string
  completeness: number
  uncertainty: number
}

export interface AttributionResult {
  site_id: string
  confidence: ConfidenceLevel
  confidence_score: number
  evidence: string[]
  warning: string
}

export interface ExportRequest {
  job_id: string
  format: 'report' | 'geojson' | 'csv' | 'timelapse'
  site_ids: string[]
}

export interface ExportArtifact {
  job_id: string
  format: 'report' | 'geojson' | 'csv' | 'timelapse'
  filename: string
  download_url: string
}

export interface AnalysisSummary {
  job_id: string
  city: CityAOI
  polygons_count: number
  atmospheric_zones_count: number
  attribution: AttributionResult[]
  layers: LayerMetadata[]
  temporal_years: number[]
  temporal_note: string
}

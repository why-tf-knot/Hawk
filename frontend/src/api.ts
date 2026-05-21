import type { AnalysisSummary, CityAOI, ExportArtifact, ExportRequest, IndustrialPolygon, TimeSeriesPoint } from './types'

const API_BASE = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000'

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: { 'Content-Type': 'application/json', ...(options?.headers ?? {}) },
    ...options,
  })
  if (!response.ok) {
    throw new Error(`${response.status} ${response.statusText}`)
  }
  return response.json() as Promise<T>
}

export const api = {
  health: () => request<{ status: string }>('/health'),
  searchCities: async (query: string) => request<{ results: CityAOI[] }>(`/cities/search?q=${encodeURIComponent(query)}`),
  analyzeCity: async (cityQuery: string, startDate: string, endDate: string) =>
    request<{ job_id: string; status: string }>('/analysis/city', {
      method: 'POST',
      body: JSON.stringify({ city_query: cityQuery, start_date: startDate, end_date: endDate }),
    }),
  getStatus: (jobId: string) => request<{ status: string }>(`/analysis/${jobId}/status`),
  getSummary: (jobId: string) => request<AnalysisSummary>(`/analysis/${jobId}/summary`),
  getPolygons: (jobId: string) => request<IndustrialPolygon[]>(`/analysis/${jobId}/polygons`),
  getTimeseries: (jobId: string, siteId: string) => request<TimeSeriesPoint[]>(`/analysis/${jobId}/timeseries?site_id=${siteId}`),
  getTileUrl: (jobId: string, layer: string) => request<{ tile_url: string }>(`/analysis/${jobId}/tiles/${layer}`),
  getLegend: (jobId: string, layer: string) => request<Record<string, unknown>>(`/analysis/${jobId}/legend/${layer}`),
  exportData: (path: 'report' | 'geojson' | 'csv', body: ExportRequest) =>
    request<ExportArtifact>(`/exports/${path}`, { method: 'POST', body: JSON.stringify(body) }),
}

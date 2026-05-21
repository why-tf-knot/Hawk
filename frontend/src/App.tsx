import { useMemo, useState } from 'react'
import './App.css'
import { api } from './api'
import { CitySearchBar } from './components/CitySearchBar'
import { ExportModal } from './components/ExportModal'
import { LayerControlPanel } from './components/LayerControlPanel'
import { MapCanvas } from './components/MapCanvas'
import { MapLegend } from './components/MapLegend'
import { SiteDetailsDrawer } from './components/SiteDetailsDrawer'
import { SiteListPanel } from './components/SiteListPanel'
import { TimeSlider } from './components/TimeSlider'
import { TrendCharts } from './components/TrendCharts'
import type { AnalysisSummary, CityAOI, IndustrialPolygon, TimeSeriesPoint } from './types'

function App() {
  const [cities, setCities] = useState<CityAOI[]>([])
  const [jobId, setJobId] = useState<string>()
  const [summary, setSummary] = useState<AnalysisSummary>()
  const [polygons, setPolygons] = useState<IndustrialPolygon[]>([])
  const [selectedSiteId, setSelectedSiteId] = useState<string>()
  const [timeseries, setTimeseries] = useState<TimeSeriesPoint[]>([])
  const [timeFrame, setTimeFrame] = useState(0)
  const [enabledLayers, setEnabledLayers] = useState<Record<string, boolean>>({
    optical_composite: true,
    radar: true,
    thermal: false,
    atmospheric_anomaly: true,
    confidence: true,
  })
  const [status, setStatus] = useState('Ready')

  const selectedCity = summary?.city
  const selectedSite = useMemo(
    () => polygons.find((polygon) => polygon.site_id === selectedSiteId),
    [polygons, selectedSiteId],
  )

  const searchCities = async (query: string) => {
    setStatus('Searching cities...')
    const response = await api.searchCities(query)
    setCities(response.results)
    setStatus(response.results.length ? 'Select a city and analyze.' : 'No cities found.')
  }

  const analyzeCity = async (cityName: string) => {
    setStatus('Submitting analysis...')
    const analysis = await api.analyzeCity(cityName, '2018-01-01', '2025-12-31')
    setJobId(analysis.job_id)
    const summaryResponse = await api.getSummary(analysis.job_id)
    setSummary(summaryResponse)
    const polygonResponse = await api.getPolygons(analysis.job_id)
    setPolygons(polygonResponse)
    setSelectedSiteId(polygonResponse[0]?.site_id)
    if (polygonResponse[0]) {
      const ts = await api.getTimeseries(analysis.job_id, polygonResponse[0].site_id)
      setTimeseries(ts)
    }
    setStatus('Analysis complete with uncertainty-aware outputs.')
  }

  const selectSite = async (siteId: string) => {
    setSelectedSiteId(siteId)
    if (jobId) {
      const ts = await api.getTimeseries(jobId, siteId)
      setTimeseries(ts)
    }
  }

  const toggleLayer = (layerName: string) => {
    setEnabledLayers((previous) => ({ ...previous, [layerName]: !previous[layerName] }))
  }

  return (
    <main className="app-shell">
      <aside className="left-panel">
        <h1>Hawk</h1>
        <p className="muted">Industrial activity and atmospheric anomaly monitoring.</p>
        <CitySearchBar cities={cities} onSearch={searchCities} onAnalyze={analyzeCity} />
        <LayerControlPanel layers={summary?.layers ?? []} enabledLayers={enabledLayers} onToggle={toggleLayer} />
        <SiteListPanel sites={polygons} onSelect={selectSite} />
        <ExportModal jobId={jobId} />
      </aside>

      <section className="map-section">
        <MapCanvas city={selectedCity} polygons={polygons} selectedSiteId={selectedSiteId} onSelectSite={selectSite} />
        <MapLegend layers={summary?.layers ?? []} />
        <SiteDetailsDrawer site={selectedSite} timeseries={timeseries} />
      </section>

      <section className="bottom-panel">
        <TimeSlider value={timeFrame} onChange={setTimeFrame} max={Math.max((summary?.temporal_years.length ?? 1) - 1, 1)} />
        <TrendCharts points={timeseries} availableYears={summary?.temporal_years} note={summary?.temporal_note} />
        <div className="status">{status}</div>
      </section>
    </main>
  )
}

export default App

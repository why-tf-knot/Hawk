import { useState } from 'react'
import { api } from '../api'

interface Props {
  jobId?: string
}

export function ExportModal({ jobId }: Props) {
  const [message, setMessage] = useState('')

  if (!jobId) {
    return <section className="panel-section">Run analysis to enable exports.</section>
  }

  const handleExport = async (format: 'report' | 'geojson' | 'csv' | 'timelapse') => {
    const artifact = await api.exportData(format, { job_id: jobId, format, site_ids: [] })
    setMessage(`Prepared: ${artifact.filename}`)
  }

  return (
    <section className="panel-section">
      <h2>Export modal</h2>
      <div className="export-buttons">
        <button type="button" onClick={() => handleExport('report')}>Report</button>
        <button type="button" onClick={() => handleExport('geojson')}>GeoJSON</button>
        <button type="button" onClick={() => handleExport('csv')}>CSV</button>
        <button type="button" onClick={() => handleExport('timelapse')}>Time-lapse video</button>
      </div>
      {message ? <p>{message}</p> : null}
    </section>
  )
}

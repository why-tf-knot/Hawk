import { useState } from 'react'
import type { FormEvent } from 'react'
import type { CityAOI } from '../types'

interface Props {
  cities: CityAOI[]
  onSearch: (query: string) => Promise<void>
  onAnalyze: (cityName: string) => Promise<void>
}

export function CitySearchBar({ cities, onSearch, onAnalyze }: Props) {
  const [query, setQuery] = useState('Mumbai')

  const submitSearch = async (event: FormEvent) => {
    event.preventDefault()
    await onSearch(query)
  }

  return (
    <section className="panel-section">
      <h2>City search</h2>
      <form onSubmit={submitSearch} className="city-search">
        <input value={query} onChange={(e) => setQuery(e.target.value)} placeholder="Search city" />
        <button type="submit">Search</button>
      </form>
      <ul className="city-list">
        {cities.map((city) => (
          <li key={city.id}>
            <button type="button" onClick={() => onAnalyze(city.name)}>
              Analyze city: {city.name}, {city.country}
            </button>
          </li>
        ))}
      </ul>
    </section>
  )
}

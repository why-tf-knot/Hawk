from app.data.demo import DEMO_CITIES
from app.models.schemas import CityAOI


class GeocodingService:
    def search(self, query: str) -> list[CityAOI]:
        normalized = query.strip().lower()
        return [c for c in DEMO_CITIES if normalized in c.name.lower()][:10]


geocoding_service = GeocodingService()

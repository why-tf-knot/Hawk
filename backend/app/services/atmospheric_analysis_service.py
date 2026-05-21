from app.data.demo import demo_atmospheric_zones
from app.models.schemas import AtmosphericZone


class AtmosphericAnalysisService:
    def analyze(self, city_id: str, features: dict) -> list[AtmosphericZone]:
        return demo_atmospheric_zones(city_id)


atmospheric_analysis_service = AtmosphericAnalysisService()

from app.data.demo import demo_attribution
from app.models.schemas import AttributionResult


class AttributionService:
    def score(self, city_id: str) -> list[AttributionResult]:
        # TODO: Replace heuristics with interpretable model feature importances.
        return demo_attribution(city_id)


attribution_service = AttributionService()

from app.data.demo import demo_polygons
from app.models.schemas import IndustrialPolygon


class IndustrialDetectionService:
    def detect(self, city_id: str, features: dict) -> list[IndustrialPolygon]:
        # TODO: Tune classifier thresholds with labeled training data.
        return demo_polygons(city_id)


industrial_detection_service = IndustrialDetectionService()

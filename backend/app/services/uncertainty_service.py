from app.models.schemas import ConfidenceLevel


class UncertaintyService:
    def confidence_from_score(self, score: float) -> ConfidenceLevel:
        if score >= 0.75:
            return ConfidenceLevel.high
        if score >= 0.5:
            return ConfidenceLevel.medium
        return ConfidenceLevel.low


uncertainty_service = UncertaintyService()

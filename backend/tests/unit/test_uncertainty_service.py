from app.models.schemas import ConfidenceLevel
from app.services.uncertainty_service import uncertainty_service


def test_uncertainty_thresholds():
    assert uncertainty_service.confidence_from_score(0.81) == ConfidenceLevel.high
    assert uncertainty_service.confidence_from_score(0.55) == ConfidenceLevel.medium
    assert uncertainty_service.confidence_from_score(0.2) == ConfidenceLevel.low

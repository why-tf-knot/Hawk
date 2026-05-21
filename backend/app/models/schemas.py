from datetime import date, datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class ConfidenceLevel(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class CityAOI(BaseModel):
    id: str
    name: str
    country: str
    center: tuple[float, float]
    bbox: tuple[float, float, float, float]
    geojson: dict[str, Any]


class QualityMetadata(BaseModel):
    source_resolution_m: float
    masking_fraction: float = Field(ge=0, le=1)
    valid_observations: int
    qa_notes: list[str] = Field(default_factory=list)


class LayerMetadata(BaseModel):
    layer_name: str
    title: str
    unit: str | None = None
    native_resolution_m: float
    scale_warning: str
    quality: QualityMetadata


class SiteMetrics(BaseModel):
    site_id: str
    area_sq_km: float
    industrial_score: float = Field(ge=0, le=1)
    thermal_anomaly_index: float | None = None
    completeness: float = Field(ge=0, le=1)


class IndustrialPolygon(BaseModel):
    site_id: str
    city_id: str
    class_name: str
    confidence: ConfidenceLevel
    confidence_score: float = Field(ge=0, le=1)
    geometry: dict[str, Any]
    metrics: SiteMetrics
    quality: QualityMetadata


class AtmosphericZone(BaseModel):
    zone_id: str
    site_id: str
    zone_type: str
    geometry: dict[str, Any]
    quality: QualityMetadata


class AttributionResult(BaseModel):
    site_id: str
    confidence: ConfidenceLevel
    confidence_score: float = Field(ge=0, le=1)
    evidence: list[str]
    warning: str


class TimeSeriesPoint(BaseModel):
    date: date
    value: float
    metric: str
    completeness: float = Field(ge=0, le=1)
    uncertainty: float = Field(ge=0)


class AnalysisCityRequest(BaseModel):
    city_query: str
    start_date: date
    end_date: date


class AnalysisJobStatus(BaseModel):
    job_id: str
    status: str
    started_at: datetime
    finished_at: datetime | None = None
    message: str | None = None


class AnalysisSummary(BaseModel):
    job_id: str
    city: CityAOI
    polygons_count: int
    atmospheric_zones_count: int
    attribution: list[AttributionResult]
    layers: list[LayerMetadata]
    temporal_years: list[int]
    temporal_note: str


class ExportFormat(str, Enum):
    report = "report"
    geojson = "geojson"
    csv = "csv"
    timelapse = "timelapse"


class ExportRequest(BaseModel):
    job_id: str
    format: ExportFormat
    site_ids: list[str] = Field(default_factory=list)


class ExportArtifact(BaseModel):
    job_id: str
    format: ExportFormat
    filename: str
    download_url: str


class CitySearchResponse(BaseModel):
    results: list[CityAOI]


class AnalysisCityResponse(BaseModel):
    job_id: str
    status: str

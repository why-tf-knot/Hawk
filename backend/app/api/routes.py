from datetime import UTC, datetime
from uuid import uuid4

from fastapi import APIRouter, BackgroundTasks, HTTPException, Query

from app.data.demo import demo_timeseries
from app.models.schemas import (
    AnalysisCityRequest,
    AnalysisCityResponse,
    AnalysisJobStatus,
    AnalysisSummary,
    CitySearchResponse,
    ExportArtifact,
    ExportRequest,
    IndustrialPolygon,
    TimeSeriesPoint,
)
from app.services.atmospheric_analysis_service import atmospheric_analysis_service
from app.services.attribution_service import attribution_service
from app.services.cache_service import JobRecord, cache_service
from app.services.earth_engine_service import earth_engine_service
from app.services.export_service import export_service
from app.services.geocoding_service import geocoding_service
from app.services.industrial_detection_service import industrial_detection_service
from app.services.preprocessing_service import preprocessing_service
from app.services.tile_service import tile_service

router = APIRouter()


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/cities/search", response_model=CitySearchResponse)
def city_search(q: str = Query(min_length=2)) -> CitySearchResponse:
    return CitySearchResponse(results=geocoding_service.search(q))


def _run_analysis(job_id: str, payload: AnalysisCityRequest) -> None:
    city = geocoding_service.search(payload.city_query)
    if not city:
        record = cache_service.get_job(job_id)
        if record:
            record.status = "failed"
            record.finished_at = datetime.now(UTC)
            record.message = "City not found"
        return

    selected = city[0]
    preprocessed = preprocessing_service.run(selected.geojson, payload.start_date, payload.end_date)
    industrial_features = earth_engine_service.build_industrial_features(preprocessed)
    atmospheric_features = earth_engine_service.build_atmospheric_features(preprocessed)
    polygons = industrial_detection_service.detect(selected.id, industrial_features)
    zones = atmospheric_analysis_service.analyze(selected.id, atmospheric_features)
    attribution = attribution_service.score(selected.id)

    record = cache_service.get_job(job_id)
    if not record:
        return

    record.status = "completed"
    record.finished_at = datetime.now(UTC)
    record.payload = {
        "city": selected.model_dump(),
        "polygons": [p.model_dump() for p in polygons],
        "zones": [z.model_dump() for z in zones],
        "attribution": [a.model_dump() for a in attribution],
        "layers": [l.model_dump() for l in tile_service.layers_metadata()],
    }


@router.post("/analysis/city", response_model=AnalysisCityResponse)
def analyze_city(request: AnalysisCityRequest, background_tasks: BackgroundTasks) -> AnalysisCityResponse:
    job_id = str(uuid4())
    cache_service.set_job(job_id, JobRecord(status="queued", started_at=datetime.now(UTC)))
    background_tasks.add_task(_run_analysis, job_id, request)
    return AnalysisCityResponse(job_id=job_id, status="queued")


@router.get("/analysis/{job_id}/status", response_model=AnalysisJobStatus)
def analysis_status(job_id: str) -> AnalysisJobStatus:
    record = cache_service.get_job(job_id)
    if not record:
        raise HTTPException(status_code=404, detail="Job not found")
    return AnalysisJobStatus(
        job_id=job_id,
        status=record.status,
        started_at=record.started_at,
        finished_at=record.finished_at,
        message=record.message,
    )


@router.get("/analysis/{job_id}/summary", response_model=AnalysisSummary)
def analysis_summary(job_id: str) -> AnalysisSummary:
    record = cache_service.get_job(job_id)
    if not record or record.status != "completed":
        raise HTTPException(status_code=404, detail="Summary unavailable")
    payload = record.payload
    return AnalysisSummary(
        job_id=job_id,
        city=payload["city"],
        polygons_count=len(payload["polygons"]),
        atmospheric_zones_count=len(payload["zones"]),
        attribution=payload["attribution"],
        layers=payload["layers"],
    )


@router.get("/analysis/{job_id}/polygons", response_model=list[IndustrialPolygon])
def analysis_polygons(job_id: str) -> list[IndustrialPolygon]:
    record = cache_service.get_job(job_id)
    if not record or record.status != "completed":
        raise HTTPException(status_code=404, detail="Polygons unavailable")
    return [IndustrialPolygon(**p) for p in record.payload["polygons"]]


@router.get("/analysis/{job_id}/timeseries", response_model=list[TimeSeriesPoint])
def analysis_timeseries(job_id: str, site_id: str = Query(min_length=1)) -> list[TimeSeriesPoint]:
    record = cache_service.get_job(job_id)
    if not record or record.status != "completed":
        raise HTTPException(status_code=404, detail="Timeseries unavailable")
    return demo_timeseries(site_id)


@router.get("/analysis/{job_id}/tiles/{layer_name}")
def analysis_tiles(job_id: str, layer_name: str) -> dict[str, str]:
    record = cache_service.get_job(job_id)
    if not record or record.status != "completed":
        raise HTTPException(status_code=404, detail="Tiles unavailable")
    return {"layer_name": layer_name, "tile_url": tile_service.layer_tile_url(job_id, layer_name)}


@router.get("/analysis/{job_id}/legend/{layer_name}")
def analysis_legend(job_id: str, layer_name: str) -> dict:
    record = cache_service.get_job(job_id)
    if not record or record.status != "completed":
        raise HTTPException(status_code=404, detail="Legend unavailable")
    return tile_service.layer_legend(layer_name)


@router.post("/exports/report", response_model=ExportArtifact)
def export_report(request: ExportRequest) -> ExportArtifact:
    return export_service.create_artifact(request.job_id, request.format)


@router.post("/exports/geojson", response_model=ExportArtifact)
def export_geojson(request: ExportRequest) -> ExportArtifact:
    return export_service.create_artifact(request.job_id, request.format)


@router.post("/exports/csv", response_model=ExportArtifact)
def export_csv(request: ExportRequest) -> ExportArtifact:
    return export_service.create_artifact(request.job_id, request.format)

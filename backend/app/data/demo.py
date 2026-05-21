from datetime import date

from app.models.schemas import (
    AtmosphericZone,
    AttributionResult,
    CityAOI,
    ConfidenceLevel,
    IndustrialPolygon,
    LayerMetadata,
    QualityMetadata,
    SiteMetrics,
    TimeSeriesPoint,
)

DEMO_CITIES = [
    CityAOI(
        id="mumbai-in",
        name="Mumbai",
        country="India",
        center=(19.0760, 72.8777),
        bbox=(72.74, 18.89, 73.05, 19.32),
        geojson={
            "type": "Polygon",
            "coordinates": [[
                [72.74, 18.89],
                [73.05, 18.89],
                [73.05, 19.32],
                [72.74, 19.32],
                [72.74, 18.89],
            ]],
        },
    ),
    CityAOI(
        id="houston-us",
        name="Houston",
        country="United States",
        center=(29.7604, -95.3698),
        bbox=(-95.8, 29.4, -94.9, 30.2),
        geojson={
            "type": "Polygon",
            "coordinates": [[
                [-95.8, 29.4],
                [-94.9, 29.4],
                [-94.9, 30.2],
                [-95.8, 30.2],
                [-95.8, 29.4],
            ]],
        },
    ),
]


def quality(resolution: float, masking_fraction: float, valid_observations: int, notes: list[str]) -> QualityMetadata:
    return QualityMetadata(
        source_resolution_m=resolution,
        masking_fraction=masking_fraction,
        valid_observations=valid_observations,
        qa_notes=notes,
    )


def demo_polygons(city_id: str) -> list[IndustrialPolygon]:
    q_surface = quality(10, 0.12, 28, ["Sentinel-2 L2A cloud/shadow mask", "Sentinel-1 VV/VH continuity"])
    return [
        IndustrialPolygon(
            site_id=f"{city_id}-site-001",
            city_id=city_id,
            class_name="industrial activity",
            confidence=ConfidenceLevel.high,
            confidence_score=0.82,
            geometry={
                "type": "Polygon",
                "coordinates": [[
                    [72.88, 19.02], [72.90, 19.02], [72.90, 19.04], [72.88, 19.04], [72.88, 19.02]
                ]],
            },
            metrics=SiteMetrics(
                site_id=f"{city_id}-site-001",
                area_sq_km=2.7,
                industrial_score=0.88,
                thermal_anomaly_index=0.52,
                completeness=0.86,
            ),
            quality=q_surface,
        ),
        IndustrialPolygon(
            site_id=f"{city_id}-site-002",
            city_id=city_id,
            class_name="industrial activity",
            confidence=ConfidenceLevel.medium,
            confidence_score=0.63,
            geometry={
                "type": "Polygon",
                "coordinates": [[
                    [72.92, 19.08], [72.94, 19.08], [72.94, 19.10], [72.92, 19.10], [72.92, 19.08]
                ]],
            },
            metrics=SiteMetrics(
                site_id=f"{city_id}-site-002",
                area_sq_km=1.9,
                industrial_score=0.67,
                thermal_anomaly_index=0.31,
                completeness=0.77,
            ),
            quality=q_surface,
        ),
    ]


def demo_atmospheric_zones(city_id: str) -> list[AtmosphericZone]:
    q = quality(
        7000,
        0.15,
        14,
        [
            "Sentinel-5P QA filtered; native coarse resolution",
            "Use zone-level interpretation only, not rooftop attribution",
        ],
    )
    return [
        AtmosphericZone(
            zone_id=f"{city_id}-atm-downwind-001",
            site_id=f"{city_id}-site-001",
            zone_type="downwind",
            geometry={
                "type": "Polygon",
                "coordinates": [[
                    [72.89, 19.04], [72.95, 19.04], [72.95, 19.12], [72.89, 19.12], [72.89, 19.04]
                ]],
            },
            quality=q,
        )
    ]


def demo_attribution(city_id: str) -> list[AttributionResult]:
    return [
        AttributionResult(
            site_id=f"{city_id}-site-001",
            confidence=ConfidenceLevel.medium,
            confidence_score=0.68,
            evidence=[
                "Persistent Sentinel-1/2 industrial signature",
                "Downwind atmospheric anomaly exceeds upwind baseline",
                "Signal persists for >3 monthly composites",
            ],
            warning="Atmospheric indicators are coarse-resolution and probabilistic; avoid rooftop-level claims.",
        )
    ]


def demo_timeseries(site_id: str) -> list[TimeSeriesPoint]:
    return [
        TimeSeriesPoint(date=date(2025, 1, 1), value=0.12, metric="atmospheric anomaly", completeness=0.81, uncertainty=0.04),
        TimeSeriesPoint(date=date(2025, 2, 1), value=0.14, metric="atmospheric anomaly", completeness=0.79, uncertainty=0.05),
        TimeSeriesPoint(date=date(2025, 3, 1), value=0.16, metric="atmospheric anomaly", completeness=0.83, uncertainty=0.04),
    ]


def demo_layers() -> list[LayerMetadata]:
    return [
        LayerMetadata(
            layer_name="optical_composite",
            title="Optical composite (Sentinel-2)",
            native_resolution_m=10,
            unit=None,
            scale_warning="Surface layer at ~10 m supports polygon-level site mapping.",
            quality=quality(10, 0.12, 28, ["Cloud-aware median composite"]),
        ),
        LayerMetadata(
            layer_name="radar",
            title="Radar structure (Sentinel-1 VV/VH)",
            native_resolution_m=10,
            unit="dB",
            scale_warning="All-weather structural context layer.",
            quality=quality(10, 0.08, 36, ["Terrain corrected, despeckled"]),
        ),
        LayerMetadata(
            layer_name="thermal",
            title="Thermal context (Landsat 8/9)",
            native_resolution_m=30,
            unit="K",
            scale_warning="Thermal context for area-level heat anomalies.",
            quality=quality(30, 0.18, 20, ["Cloud filtered Landsat L2 composite"]),
        ),
        LayerMetadata(
            layer_name="atmospheric_anomaly",
            title="Atmospheric anomaly (Sentinel-5P)",
            native_resolution_m=7000,
            unit="mol/m²",
            scale_warning="Coarse atmospheric product. Interpretable only for zone-level trends, not rooftops.",
            quality=quality(7000, 0.15, 14, ["QA filtered (qa_value threshold)"]),
        ),
        LayerMetadata(
            layer_name="confidence",
            title="Attribution confidence",
            native_resolution_m=250,
            unit="score",
            scale_warning="Confidence combines multi-evidence attribution and uncertainty controls.",
            quality=quality(250, 0.0, 1, ["Model-derived confidence, not direct measurement"]),
        ),
    ]

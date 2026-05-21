from datetime import date


class EarthEngineService:
    """Earth Engine wrapper service.

    Functions document the native scale and scientific limits.
    In mock mode they return deterministic metadata while keeping
    the same signatures used by live Earth Engine integrations.
    """

    def sentinel2_preprocess(self, aoi: dict, start_date: date, end_date: date) -> dict:
        """Sentinel-2 L2A preprocess at ~10 m; strict cloud/shadow/cirrus masking."""
        return {"dataset": "COPERNICUS/S2_SR_HARMONIZED", "native_resolution_m": 10}

    def sentinel1_preprocess(self, aoi: dict, start_date: date, end_date: date) -> dict:
        """Sentinel-1 GRD preprocess at ~10 m with terrain correction and speckle handling."""
        return {"dataset": "COPERNICUS/S1_GRD", "native_resolution_m": 10}

    def landsat_preprocess(self, aoi: dict, start_date: date, end_date: date) -> dict:
        """Landsat 8/9 L2 preprocess at 30 m for thermal context and long-term continuity."""
        return {"dataset": "LANDSAT/LC08/C02/T1_L2 + LC09", "native_resolution_m": 30}

    def sentinel5p_preprocess(self, aoi: dict, start_date: date, end_date: date) -> dict:
        """Sentinel-5P CH4 preprocess at coarse native scale (~7 km), QA-filtered only."""
        return {"dataset": "COPERNICUS/S5P/OFFL/L3_CH4", "native_resolution_m": 7000}

    def build_industrial_features(self, preprocessed: dict) -> dict:
        return {"features": ["optical_stats", "swir_nir_ratios", "vv_vh_texture", "thermal_context"]}

    def build_atmospheric_features(self, preprocessed: dict) -> dict:
        return {"features": ["zone_mean", "upwind_downwind_contrast", "qa_weighted_anomaly"]}

    def compute_polygon_stats(self, polygons: list[dict], features: dict) -> dict:
        return {"polygon_count": len(polygons), "stats_ready": True}

    def compute_influence_zone_stats(self, zones: list[dict], features: dict) -> dict:
        return {"zone_count": len(zones), "stats_ready": True}

    def create_timeseries(self, target_id: str, metric: str) -> dict:
        return {"target_id": target_id, "metric": metric, "method": "monthly_median"}

    def get_tile_url(self, layer_name: str, job_id: str) -> str:
        """Returns XYZ tile URL generated from processed Earth Engine visualization."""
        return f"https://tiles.hawk.local/{job_id}/{layer_name}/{{z}}/{{x}}/{{y}}.png"


earth_engine_service = EarthEngineService()

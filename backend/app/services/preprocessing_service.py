from datetime import date

from app.services.earth_engine_service import earth_engine_service


class PreprocessingService:
    def run(self, aoi: dict, start_date: date, end_date: date) -> dict:
        return {
            "sentinel2": earth_engine_service.sentinel2_preprocess(aoi, start_date, end_date),
            "sentinel1": earth_engine_service.sentinel1_preprocess(aoi, start_date, end_date),
            "landsat": earth_engine_service.landsat_preprocess(aoi, start_date, end_date),
            "sentinel5p": earth_engine_service.sentinel5p_preprocess(aoi, start_date, end_date),
            "dem": {"dataset": "USGS/SRTMGL1_003", "native_resolution_m": 30},
        }


preprocessing_service = PreprocessingService()

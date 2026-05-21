from app.data.demo import demo_layers
from app.services.earth_engine_service import earth_engine_service


class TileService:
    def layer_tile_url(self, job_id: str, layer_name: str) -> str:
        return earth_engine_service.get_tile_url(layer_name, job_id)

    def layer_legend(self, layer_name: str) -> dict:
        legends = {
            "industrial_polygons": {"type": "categorical", "items": [{"label": "industrial activity", "color": "#ef4444"}]},
            "atmospheric_anomaly": {
                "type": "ramp",
                "items": [
                    {"label": "low", "color": "#93c5fd"},
                    {"label": "medium", "color": "#f59e0b"},
                    {"label": "high", "color": "#dc2626"},
                ],
                "warning": "Layer is coarse and should be interpreted over zones, not rooftops.",
            },
        }
        return legends.get(layer_name, {"type": "metadata", "items": []})

    def layers_metadata(self):
        return demo_layers()


tile_service = TileService()

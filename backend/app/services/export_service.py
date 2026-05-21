from app.models.schemas import ExportArtifact, ExportFormat


class ExportService:
    def create_artifact(self, job_id: str, fmt: ExportFormat) -> ExportArtifact:
        extension = "json" if fmt == ExportFormat.geojson else "csv" if fmt == ExportFormat.csv else "pdf"
        return ExportArtifact(
            job_id=job_id,
            format=fmt,
            filename=f"hawk_{job_id}.{extension}",
            download_url=f"/downloads/hawk_{job_id}.{extension}",
        )


export_service = ExportService()

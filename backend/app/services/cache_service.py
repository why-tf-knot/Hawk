from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class JobRecord:
    status: str
    started_at: datetime
    finished_at: datetime | None = None
    payload: dict[str, Any] = field(default_factory=dict)
    message: str | None = None


class CacheService:
    def __init__(self) -> None:
        self._jobs: dict[str, JobRecord] = {}

    def set_job(self, job_id: str, record: JobRecord) -> None:
        self._jobs[job_id] = record

    def get_job(self, job_id: str) -> JobRecord | None:
        return self._jobs.get(job_id)


cache_service = CacheService()

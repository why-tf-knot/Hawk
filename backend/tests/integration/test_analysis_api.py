from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_analysis_workflow_happy_path():
    response = client.post(
        "/analysis/city",
        json={"city_query": "mumbai", "start_date": "2025-01-01", "end_date": "2025-03-31"},
    )
    assert response.status_code == 200
    job_id = response.json()["job_id"]

    status = client.get(f"/analysis/{job_id}/status")
    assert status.status_code == 200

    summary = client.get(f"/analysis/{job_id}/summary")
    assert summary.status_code == 200
    assert summary.json()["polygons_count"] >= 1
    assert len(summary.json()["temporal_years"]) >= 5

    polygons = client.get(f"/analysis/{job_id}/polygons")
    assert polygons.status_code == 200
    assert len(polygons.json()) >= 1

    site_id = polygons.json()[0]["site_id"]
    timeseries = client.get(f"/analysis/{job_id}/timeseries", params={"site_id": site_id})
    assert timeseries.status_code == 200
    assert len(timeseries.json()) >= 5

    timelapse = client.post(
        "/exports/timelapse",
        json={"job_id": job_id, "format": "timelapse", "site_ids": [site_id]},
    )
    assert timelapse.status_code == 200
    assert timelapse.json()["filename"].endswith(".mp4")

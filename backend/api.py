from typing import Any, Optional

from fastapi import FastAPI, Query

from di import build_import_service


def create_app(db_url: Optional[str] = None) -> FastAPI:
    if not db_url:
        db_url = "sqlite:///app.db"

    service = build_import_service(db_url)
    app = FastAPI(title="SoftDocLab API", version="1.0.0")

    @app.get("/")
    def root_info() -> dict[str, Any]:
        return {
                "/docs": "Swagger",
                "/patients/count": "Number of patients in database",
                "/patients": "List of patients ",
                "/studies": "List of studies"
                }

    @app.get("/patients/count")
    def patient_count() -> dict[str, int]:
        return {"count": service.count_patients()}

    @app.get("/patients")
    def list_patients(limit: int = Query(100, ge=1, le=1000)) -> list[dict[str, Any]]:
        return service.list_patients(limit)

    @app.get("/studies")
    def list_studies(limit: int = Query(100, ge=1, le=1000)) -> list[dict[str, Any]]:
        return service.list_studies(limit)

    return app


app = create_app()

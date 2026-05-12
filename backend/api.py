from pathlib import Path
from typing import Any, Optional

from fastapi import FastAPI, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from di import build_import_service
from interfaces import StudyPayload


class StudyInput(BaseModel):
    patient_first_name: str = Field(min_length=1, max_length=100)
    patient_last_name: str = Field(min_length=1, max_length=100)
    patient_email: str = Field(min_length=1, max_length=200)
    doctor_name: str = Field(min_length=1, max_length=120)
    specialization: str = Field(min_length=1, max_length=120)
    status: str = Field(min_length=1, max_length=50)
    report_text: str = Field(min_length=1, max_length=2000)
    study_file_name: str = Field(min_length=1, max_length=200)


def create_app(db_url: Optional[str] = None) -> FastAPI:
    if not db_url:
        db_url = "sqlite:///app.db"

    service = build_import_service(db_url)
    app = FastAPI(title="SoftDocLab API", version="1.0.0")
    ui_dir = Path(__file__).resolve().parent / "ui"
    if ui_dir.exists():
        app.mount("/ui", StaticFiles(directory=str(ui_dir), html=True), name="ui")

    def to_payload(data: StudyInput) -> StudyPayload:
        raw = data.model_dump() if hasattr(data, "model_dump") else data.dict()
        return StudyPayload(**raw)

    @app.get("/")
    def root_info() -> dict[str, Any]:
        return {
            "/docs": "Swagger",
            "/ui": "Web UI",
            "/patients/count": "Number of patients in database",
            "/patients": "List of patients",
            "/studies/count": "Number of studies in database",
            "/studies": "List of studies",
        }

    @app.get("/patients/count")
    def patient_count() -> dict[str, int]:
        return {"count": service.count_patients()}

    @app.get("/studies/count")
    def study_count() -> dict[str, int]:
        return {"count": service.count_studies()}

    @app.get("/patients")
    def list_patients(limit: int = Query(100, ge=1, le=1000)) -> list[dict[str, Any]]:
        return service.list_patients(limit)

    @app.get("/studies")
    def list_studies(
        limit: int = Query(100, ge=1, le=1000),
        offset: int = Query(0, ge=0),
    ) -> list[dict[str, Any]]:
        return service.list_studies(limit, offset)

    @app.get("/studies/{study_id}")
    def get_study(study_id: int) -> dict[str, Any]:
        study = service.get_study(study_id)
        if study is None:
            raise HTTPException(status_code=404, detail="Study not found")
        return study

    @app.post("/studies")
    def create_study(payload: StudyInput) -> dict[str, Any]:
        return service.create_study(to_payload(payload))

    @app.put("/studies/{study_id}")
    def update_study(study_id: int, payload: StudyInput) -> dict[str, Any]:
        updated = service.update_study(study_id, to_payload(payload))
        if updated is None:
            raise HTTPException(status_code=404, detail="Study not found")
        return updated

    @app.delete("/studies/{study_id}")
    def delete_study(study_id: int) -> dict[str, Any]:
        if not service.delete_study(study_id):
            raise HTTPException(status_code=404, detail="Study not found")
        return {"status": "deleted"}

    return app


app = create_app()

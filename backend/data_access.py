import csv
from typing import Iterable

from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker

from interfaces import IDataAccess, ImportRecord
from models import Base, Patient, Study


class SqlAlchemyDataAccess(IDataAccess):
    def __init__(self, engine: Engine, session_factory: sessionmaker) -> None:
        self._engine = engine
        self._session_factory = session_factory

    def init_db(self) -> None:
        Base.metadata.create_all(self._engine)

    def read_csv(self, file_path: str) -> list[dict[str, str]]:
        with open(file_path, "r", newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            rows: list[dict[str, str]] = []
            for row in reader:
                cleaned: dict[str, str] = {}
                for key, value in row.items():
                    if key is None:
                        continue
                    cleaned[key] = (value or "").strip()
                rows.append(cleaned)
            return rows

    def save_records(self, records: Iterable[ImportRecord], mode: str) -> int:
        if mode not in ("append", "replace"):
            raise ValueError("mode must be 'append' or 'replace'")

        self.init_db()
        inserted = 0
        with self._session_factory() as session:
            if mode == "replace":
                session.query(Study).delete()
                session.query(Patient).delete()
                session.commit()

            for record in records:
                patient = (
                    session.query(Patient)
                    .filter(Patient.email == record.email)
                    .one_or_none()
                )
                if patient is None:
                    patient = Patient(
                        first_name=record.patient_first_name,
                        last_name=record.patient_last_name,
                        email=record.email,
                    )
                    session.add(patient)
                    session.flush()

                study = Study(
                    patient_id=patient.id,
                    doctor_name=record.doctor_name,
                    specialization=record.specialization,
                    status=record.status,
                    report_text=record.report_text,
                    study_file_name=record.study_file_name,
                )
                session.add(study)
                inserted += 1

            session.commit()
        return inserted

    def get_patients(self, limit: int = 100) -> list[dict[str, object]]:
        self.init_db()
        with self._session_factory() as session:
            patients = (
                session.query(Patient)
                .order_by(Patient.id.asc())
                .limit(limit)
                .all()
            )
            return [
                {
                    "id": patient.id,
                    "first_name": patient.first_name,
                    "last_name": patient.last_name,
                    "email": patient.email,
                }
                for patient in patients
            ]

    def get_studies(self, limit: int = 100) -> list[dict[str, object]]:
        self.init_db()
        with self._session_factory() as session:
            studies = (
                session.query(Study)
                .order_by(Study.id.asc())
                .limit(limit)
                .all()
            )
            return [
                {
                    "id": study.id,
                    "patient_id": study.patient_id,
                    "patient_email": study.patient.email if study.patient else "",
                    "doctor_name": study.doctor_name,
                    "specialization": study.specialization,
                    "status": study.status,
                    "report_text": study.report_text,
                    "study_file_name": study.study_file_name,
                }
                for study in studies
            ]

    def count_patients(self) -> int:
        self.init_db()
        with self._session_factory() as session:
            return session.query(Patient).count()

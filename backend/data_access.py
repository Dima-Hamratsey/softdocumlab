import csv
from typing import Iterable, Optional

from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker

from interfaces import IDataAccess, ImportRecord, StudyPayload
from models import Base, Patient, Study


class SqlAlchemyDataAccess(IDataAccess):
    def __init__(self, engine: Engine, session_factory: sessionmaker) -> None:
        self._engine = engine
        self._session_factory = session_factory

    @staticmethod
    def _map_study(study: Study) -> dict[str, object]:
        patient = study.patient
        return {
            "id": study.id,
            "patient_id": study.patient_id,
            "patient_first_name": patient.first_name if patient else "",
            "patient_last_name": patient.last_name if patient else "",
            "patient_email": patient.email if patient else "",
            "doctor_name": study.doctor_name,
            "specialization": study.specialization,
            "status": study.status,
            "report_text": study.report_text,
            "study_file_name": study.study_file_name,
        }

    @staticmethod
    def _get_or_create_patient(
        session, payload: StudyPayload
    ) -> Patient:
        patient = (
            session.query(Patient)
            .filter(Patient.email == payload.patient_email)
            .one_or_none()
        )
        if patient is None:
            patient = Patient(
                first_name=payload.patient_first_name,
                last_name=payload.patient_last_name,
                email=payload.patient_email,
            )
            session.add(patient)
            session.flush()
        else:
            patient.first_name = payload.patient_first_name
            patient.last_name = payload.patient_last_name
        return patient

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

    def get_studies(self, limit: int = 100, offset: int = 0) -> list[dict[str, object]]:
        self.init_db()
        with self._session_factory() as session:
            studies = (
                session.query(Study)
                .order_by(Study.id.asc())
                .offset(offset)
                .limit(limit)
                .all()
            )
            return [self._map_study(study) for study in studies]

    def get_study(self, study_id: int) -> Optional[dict[str, object]]:
        self.init_db()
        with self._session_factory() as session:
            study = (
                session.query(Study)
                .filter(Study.id == study_id)
                .one_or_none()
            )
            if study is None:
                return None
            return self._map_study(study)

    def create_study(self, payload: StudyPayload) -> dict[str, object]:
        self.init_db()
        with self._session_factory() as session:
            patient = self._get_or_create_patient(session, payload)
            study = Study(
                patient_id=patient.id,
                doctor_name=payload.doctor_name,
                specialization=payload.specialization,
                status=payload.status,
                report_text=payload.report_text,
                study_file_name=payload.study_file_name,
            )
            session.add(study)
            session.commit()
            session.refresh(study)
            return self._map_study(study)

    def update_study(
        self, study_id: int, payload: StudyPayload
    ) -> Optional[dict[str, object]]:
        self.init_db()
        with self._session_factory() as session:
            study = (
                session.query(Study)
                .filter(Study.id == study_id)
                .one_or_none()
            )
            if study is None:
                return None
            patient = self._get_or_create_patient(session, payload)
            study.patient_id = patient.id
            study.doctor_name = payload.doctor_name
            study.specialization = payload.specialization
            study.status = payload.status
            study.report_text = payload.report_text
            study.study_file_name = payload.study_file_name
            session.commit()
            session.refresh(study)
            return self._map_study(study)

    def delete_study(self, study_id: int) -> bool:
        self.init_db()
        with self._session_factory() as session:
            study = (
                session.query(Study)
                .filter(Study.id == study_id)
                .one_or_none()
            )
            if study is None:
                return False
            session.delete(study)
            session.commit()
            return True

    def count_patients(self) -> int:
        self.init_db()
        with self._session_factory() as session:
            return session.query(Patient).count()

    def count_studies(self) -> int:
        self.init_db()
        with self._session_factory() as session:
            return session.query(Study).count()

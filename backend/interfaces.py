from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Optional, Sequence


@dataclass(frozen=True)
class ImportRecord:
    patient_first_name: str
    patient_last_name: str
    email: str
    doctor_name: str
    specialization: str
    status: str
    report_text: str
    study_file_name: str


@dataclass(frozen=True)
class StudyPayload:
    patient_first_name: str
    patient_last_name: str
    patient_email: str
    doctor_name: str
    specialization: str
    status: str
    report_text: str
    study_file_name: str


class IDataAccess(ABC):
    @abstractmethod
    def init_db(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def read_csv(self, file_path: str) -> list[dict[str, str]]:
        raise NotImplementedError

    @abstractmethod
    def save_records(self, records: Sequence[ImportRecord], mode: str) -> int:
        raise NotImplementedError

    @abstractmethod
    def get_patients(self, limit: int = 100) -> list[dict[str, Any]]:
        raise NotImplementedError

    @abstractmethod
    def get_studies(self, limit: int = 100, offset: int = 0) -> list[dict[str, Any]]:
        raise NotImplementedError

    @abstractmethod
    def get_study(self, study_id: int) -> Optional[dict[str, Any]]:
        raise NotImplementedError

    @abstractmethod
    def create_study(self, payload: StudyPayload) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def update_study(self, study_id: int, payload: StudyPayload) -> Optional[dict[str, Any]]:
        raise NotImplementedError

    @abstractmethod
    def delete_study(self, study_id: int) -> bool:
        raise NotImplementedError

    @abstractmethod
    def count_patients(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def count_studies(self) -> int:
        raise NotImplementedError


class IImportService(ABC):
    @abstractmethod
    def import_from_csv(self, file_path: str, mode: str = "append") -> int:
        raise NotImplementedError

    @abstractmethod
    def list_patients(self, limit: int = 100) -> list[dict[str, Any]]:
        raise NotImplementedError

    @abstractmethod
    def list_studies(self, limit: int = 100, offset: int = 0) -> list[dict[str, Any]]:
        raise NotImplementedError

    @abstractmethod
    def get_study(self, study_id: int) -> Optional[dict[str, Any]]:
        raise NotImplementedError

    @abstractmethod
    def create_study(self, payload: StudyPayload) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def update_study(self, study_id: int, payload: StudyPayload) -> Optional[dict[str, Any]]:
        raise NotImplementedError

    @abstractmethod
    def delete_study(self, study_id: int) -> bool:
        raise NotImplementedError

    @abstractmethod
    def count_patients(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def count_studies(self) -> int:
        raise NotImplementedError

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol, Sequence


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


class IDataAccess(Protocol):
    def init_db(self) -> None:
        raise NotImplementedError

    def read_csv(self, file_path: str) -> list[dict[str, str]]:
        raise NotImplementedError

    def save_records(self, records: Sequence[ImportRecord], mode: str) -> int:
        raise NotImplementedError

    def get_patients(self, limit: int = 100) -> list[dict[str, Any]]:
        raise NotImplementedError

    def get_studies(self, limit: int = 100) -> list[dict[str, Any]]:
        raise NotImplementedError

    def count_patients(self) -> int:
        raise NotImplementedError


class IImportService(Protocol):
    def import_from_csv(self, file_path: str, mode: str = "append") -> int:
        raise NotImplementedError

    def list_patients(self, limit: int = 100) -> list[dict[str, Any]]:
        raise NotImplementedError

    def list_studies(self, limit: int = 100) -> list[dict[str, Any]]:
        raise NotImplementedError

    def count_patients(self) -> int:
        raise NotImplementedError

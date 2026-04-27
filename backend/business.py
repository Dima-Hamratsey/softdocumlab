from typing import Optional

from interfaces import IDataAccess, IImportService, ImportRecord


class ImportService(IImportService):
    def __init__(self, data_access: IDataAccess) -> None:
        self._data_access = data_access

    def import_from_csv(self, file_path: str, mode: str = "append") -> int:
        rows = self._data_access.read_csv(file_path)
        records: list[ImportRecord] = []
        for row in rows:
            record = self._map_row(row)
            if record is not None:
                records.append(record)
        return self._data_access.save_records(records, mode)

    def list_patients(self, limit: int = 100) -> list[dict[str, object]]:
        return self._data_access.get_patients(limit)

    def list_studies(self, limit: int = 100) -> list[dict[str, object]]:
        return self._data_access.get_studies(limit)

    def count_patients(self) -> int:
        return self._data_access.count_patients()

    def _map_row(self, row: dict[str, str]) -> Optional[ImportRecord]:
        email = self._clean(row.get("email", ""))
        if not email:
            return None
        return ImportRecord(
            patient_first_name=self._clean(row.get("patient_first_name", "")),
            patient_last_name=self._clean(row.get("patient_last_name", "")),
            email=email,
            doctor_name=self._clean(row.get("doctor_name", "")),
            specialization=self._clean(row.get("specialization", "")),
            status=self._clean(row.get("status", "")),
            report_text=self._clean(row.get("report_text", "")),
            study_file_name=self._clean(row.get("study_file_name", "")),
        )

    @staticmethod
    def _clean(value: str) -> str:
        return value.strip()

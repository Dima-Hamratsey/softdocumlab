from typing import Any, Protocol


class IPresentation(Protocol):
    def get_root_info(self) -> dict[str, Any]:
        raise NotImplementedError

    def get_patient_count(self) -> dict[str, Any]:
        raise NotImplementedError

    def list_patients(self, limit: int = 100) -> list[dict[str, Any]]:
        raise NotImplementedError

    def list_studies(self, limit: int = 100) -> list[dict[str, Any]]:
        raise NotImplementedError

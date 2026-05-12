from abc import ABC, abstractmethod
from typing import Any


class IPresentation(ABC):
    @abstractmethod
    def get_root_info(self) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def get_patient_count(self) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def list_patients(self, limit: int = 100) -> list[dict[str, Any]]:
        raise NotImplementedError

    @abstractmethod
    def list_studies(self, limit: int = 100) -> list[dict[str, Any]]:
        raise NotImplementedError

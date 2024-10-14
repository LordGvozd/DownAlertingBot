from abc import ABC, abstractmethod

from models import ServiceInfo

class AbstractRepo(ABC):
    @abstractmethod
    def save_user(self, tg_id: str) -> None:
        pass

    @abstractmethod
    def get_all_users(self) -> list[str]:
        pass

    @abstractmethod
    def save_services_state(self, services: list[[ServiceInfo]]) -> None:
        pass

    @abstractmethod
    def get_services_state(self) -> list[ServiceInfo]:
        pass


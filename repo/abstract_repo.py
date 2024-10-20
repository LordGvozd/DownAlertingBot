from abc import ABC, abstractmethod

from schemas import ServiceInfo, User


class AbstractRepo(ABC):
    @abstractmethod
    async def save_user(self, user: User) -> None:
        pass

    @abstractmethod
    async def get_all_users(self) -> list[User]:
        pass

    @abstractmethod
    async def save_services_state(self, services: list[ServiceInfo]) -> None:
        pass

    @abstractmethod
    async def get_services_state(self) -> list[ServiceInfo]:
        pass


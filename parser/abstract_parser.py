from abc import ABC, abstractmethod

from schemas import ServiceInfo


class AbstractDownDetectorParser(ABC):
    @abstractmethod
    def get_problems_services(self) -> list[ServiceInfo]:
        raise NotImplemented

    @abstractmethod
    def get_service_info_by_name(self, service_name: str) -> ServiceInfo:
        raise NotImplemented


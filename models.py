import enum
from dataclasses import dataclass


class ServiceStatus(str, enum.Enum):
    OK = "OK"
    WARNING = "WARNING"
    ERROR = "ERROR"


@dataclass(frozen=True)
class ServiceInfo:
    service_name: str
    problem_status: ServiceStatus


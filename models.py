import enum
from dataclasses import dataclass


class ServiceStatus(str, enum.Enum):
    OK = "OK"
    WARNING = "WARNING"
    ERROR = "ERROR"


@dataclass
class ServiceInfo:
    service_name: str
    service_status: ServiceStatus

if __name__ == '__main__':
    print(ServiceInfo("l", ServiceStatus.ERROR) in [ ServiceInfo("l", ServiceStatus.OK), ])
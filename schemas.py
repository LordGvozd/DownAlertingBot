import enum
from datetime import datetime
from typing import Any

from pydantic import BaseModel

class ServiceStatus(str, enum.Enum):
    OK = "OK"
    WARNING = "WARNING"
    ERROR = "ERROR"

class User(BaseModel):
    """ User class """
    tg_id: str
    update_delay_min: int = 1
    last_update_time: datetime = datetime.now()

class ServiceInfo(BaseModel):
    """ Information about specific service """
    service_name: str
    service_status: ServiceStatus



    def __init__(self, service_name: str, service_status: ServiceStatus):
        super().__init__(service_name=service_name, service_status=service_status)


if __name__ == '__main__':
    print(ServiceInfo("l", ServiceStatus.ERROR) in [ ServiceInfo("l", ServiceStatus.OK), ])
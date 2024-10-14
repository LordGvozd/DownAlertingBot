import json
import os.path
from wsgiref.simple_server import server_version

from models import ServiceInfo, ServiceStatus
from repo.abstract_repo import AbstractRepo


class JsonRepo(AbstractRepo):

    def __init__(self, json_filename: str):
        self.__json_filename = json_filename

        self.__json = {
            "users": [],
            "state": []
        }

        if not os.path.exists(self.__json_filename):
            self.__save_json()



    def __save_json(self) -> None:
        with open(self.__json_filename, "w") as fp:
            json.dump(self.__json, fp)

    def __load_json(self) -> None:
        with open(self.__json_filename, "r") as fp:
            self.__json = json.load(fp)

    def save_user(self, tg_id: str) -> None:
        if not tg_id in self.__json["users"]:
            self.__json["users"].append(tg_id)
            self.__save_json()

    def get_all_users(self) -> list[str]:
        self.__load_json()
        return self.__json["users"]

    def save_services_state(self, services: list[ServiceInfo]) -> None:
        if not self.__json["state"]:
            for s in services:
                self.__json["state"].append({"service_name": s.service_name,
                                             "problem_status": s.problem_status.value})
                self.__save_json()

    def get_services_state(self) -> list[ServiceInfo]:
        self.__load_json()
        services = []

        for s in self.__json["state"]:
            services.append(ServiceInfo(
                s["service_name"],
                ServiceStatus(s["problem_status"])
            ))

        return services

if __name__ == '__main__':
    print(ServiceStatus.ERROR.value, ServiceStatus("ERROR"))
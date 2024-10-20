import asyncio

from  motor.motor_asyncio import AsyncIOMotorClient

from schemas import ServiceInfo, ServiceStatus, User
from repo.abstract_repo import AbstractRepo


class MongoRepo(AbstractRepo):
    def __init__(self, uri: str, db_name: str) -> None:

        self.__client = AsyncIOMotorClient(uri)
        self.__db = self.__client[db_name]

        self.__users = self.__db["users"]
        self.__services = self.__db["services"]

    async def save_user(self, user: User) -> None:
        asyncio.ensure_future(self.__users.update_one(filter={"tg_id": user.tg_id},
                                                      upsert=True,
                                                      update={
                                                          "$set": user.model_dump(exclude={"tg_id"}),
                                                          "$setOnInsert": {"tg_id": user.tg_id}
                                                      }))

    async def get_all_users(self) -> list[User]:
        users_raw = self.__users.find({}, {"_id": 0})

        users = []
        async for u in users_raw:
            users.append(User.model_validate(u))

        return users

    async def save_services_state(self, services: list[ServiceInfo]) -> None:
        for s in services:
            asyncio.ensure_future(self.__services.update_one(filter={"service_name": s.service_name},
                                       upsert=True,
                                       update={
                                           "$set": {"service_status": s.service_status.value},
                                           "$setOnInsert": {"service_name": s.service_name}
                                       }))

    async def get_services_state(self) -> list[ServiceInfo]:
        services = []
        async for s in self.__services.find({}, {"_id": 0}):
            services.append(ServiceInfo(
                service_name=s["service_name"],
                service_status=ServiceStatus(s["service_status"])
            ))

        return services

import requests as r
from bs4 import BeautifulSoup

from schemas import ServiceInfo, ServiceStatus
from parser.abstract_parser import AbstractDownDetectorParser


class DownDetectorSuParser(AbstractDownDetectorParser):
    def get_problems_services(self) -> list[ServiceInfo]:
        response = r.get(url="https://downdetector.su/")
        html = response.text

        soup = BeautifulSoup(html, "lxml")

        main_cards_container = soup.find(name="section", class_="monitor")

        warning_cards = main_cards_container.find_all("a", class_="card")
        error_cards = main_cards_container.find_all("a", class_="card down")

        error_services = [
            ServiceInfo(service_name=c["data-service"], service_status=ServiceStatus.ERROR) for c in error_cards
        ]


        warning_services = [
            ServiceInfo(service_name=c["data-service"], service_status=ServiceStatus.WARNING) for c in warning_cards
            if c["data-service"] not in [ec["data-service"] for ec in error_cards]
        ]


        return error_services + warning_services

    async def get_service_info_by_name(self, service_name: str) -> ServiceInfo:
        pass


if __name__ == '__main__':
    detector = DownDetectorSuParser()

    detector.get_problems_services()

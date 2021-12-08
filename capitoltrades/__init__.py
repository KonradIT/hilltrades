from typing import Dict, List, Optional, Union
import enum
import logging
import requests
import json
from fake_useragent import UserAgent


class PoliticalParty(str, enum.Enum):
    BOTH = "Both"
    DEMOCRAT = "Democrat"
    REPUBLICAN = "Republican"


class CongressType(str, enum.Enum):
    SENATOR = "Senator"
    REPRESENTATIVE = "Representative"


class CapitolTrades():

    def __init__(self):
        self.__url = "https://api.capitoltrades.com"
        self.__ua = UserAgent()
        self.__session = requests.Session()
        self.__session.get("https://app.capitoltrades.com/trades")
        try:
            data = self.__get_data()
        except Exception as e:
            raise Exception("Error initializing: " + str(e))
        self.__politicians = self.__parse_data(data)

    def __get_headers(self) -> Dict:

        return {
            "User-Agent": self.__ua.random,
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.5",
            "Content-Type": "application/json",
            "Origin": "https://app.capitoltrades.com",
            "DNT": "1",
            "Connection": "keep-alive",
            "Referer": "https://app.capitoltrades.com/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "Sec-GPC": "1",
            "Cache-Control": "max-age=0",
            "TE": "trailers",
        }

    def __get_data(self) -> Optional[Dict]:
        logging.debug("Getting seed data")
        params = (
            ("isTicker", "true"),
        )
        r = self.__session.get(self.__url + "/types",
                               headers=self.__get_headers(), params=params)
        r.raise_for_status()
        return r.json()

    def __parse_data(self, data: Dict) -> List[Dict]:
        logging.debug("Parsing list of politicians")

        politicians = {}
        for p in data.get("biographies", []):
            if "id" in p and "name" in p:
                politicians[p.get("id")] = p.get("name")
        return politicians

    def get_politician_id(self, name: str) -> int:
        for p in self.__politicians.keys():
            if name.lower() == self.__politicians[p].lower():
                return p
            if name.lower() == self.__politicians[p].split(",")[0].lower():
                return p
        return 0

    def trades(self, politicians: List[int],  politicianParty: PoliticalParty, congressType: CongressType, pageNumber: int = 1, pageSize: int = 20, ticker: bool = False) -> List[Dict]:

        for i in politicians:
            assert i in self.__politicians.keys()

        payload = {
            "pageNumber": pageNumber,
            "pageSize": pageSize,
            "ticker": ticker,
            "congressType": congressType,
            "politicianParty": politicianParty,
            "biographyIds": politicians,
            "gvkeys": []
        }
        r = self.__session.post(
            self.__url + "/trades", headers=self.__get_headers(), data=json.dumps(payload))
        r.raise_for_status()
        return r.json()

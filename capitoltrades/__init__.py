import logging
import requests
from typing import Any, Dict, List, Optional

from fake_useragent import UserAgent

class CapitolTrades():
    """A class for interacting with the API which supports https://capitoltrades.com."""

    def __init__(self):
        """init varz"""
        self.__url = "https://bff.capitoltrades.com"
        self.__ua = UserAgent()
        self.__session = requests.Session()
        self.__session.get("https://bff.capitoltrades.com/trades")
        try:
            data = self.__get_data()
        except Exception as e:
            raise Exception("Error initializing: " + str(e))
        self.__politicians = self.__parse_data(data)
    
    @property
    def politicians(self) -> Dict[str, str]:
        """Returns the map of politician ID to politician name of all known
        politicians on https://capitoltrades.com. Useful for debugging."""
        return self.__politicians

    def __get_headers(self) -> Dict[str, Any]:
        """Generates headers for the Capitol Trades API."""
        return {
            "User-Agent": self.__ua.random,
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.5",
            "Content-Type": "application/json",
            "Origin": "https://bff.capitoltrades.com",
            "DNT": "1",
            "Connection": "keep-alive",
            "Referer": "https://bff.capitoltrades.com/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "Sec-GPC": "1",
            "Cache-Control": "max-age=0",
            "TE": "trailers",
        }

    def __get_data(self) -> Optional[Dict]:
        """Gather data on all known politicians from https://capitoltrades.com"""
        logging.debug("Getting seed data")

        seed_data = []
        page_num = 1
        paginating = True
        while paginating:
            params = (
                ("page", page_num),
                # 100 is the max return size of the API.
                ("pageSize", 100),
            )
            r = self.__session.get(
                self.__url + "/politicians",
                headers=self.__get_headers(),
                params=params,
            )
            r.raise_for_status()

            response_json = r.json()
            data = response_json["data"]
            seed_data.extend(data)

            if len(seed_data) >= response_json["meta"]["paging"]["totalItems"] or not data:
                paginating = False
            else:
                page_num += 1

        return seed_data

    def __parse_data(self, data: Dict) -> Dict[str, str]:
        """Reformat the API data into a hash map we can use to search for politicians by name."""
        logging.debug("Parsing list of politicians")
        return {
            p["_politicianId"]: p["fullName"] for p in data
        }

    def get_politician_id(self, name: str) -> Optional[str]:
        """Search for the politician ID of the provided name."""
        for pid in self.__politicians.keys():
            if name.lower() == self.__politicians[pid].lower():
                return pid
            if name.lower() == self.__politicians[pid].split(",")[0].lower():
                return pid
        return None


    def trades(self, politician_id: str) -> List[Dict]:
        """Returns all of the trades for the provided politician ids."""
        assert politician_id in self.__politicians.keys()
        
        all_trades = []
        page_num = 1
        paginating = True
        while paginating:
            params = (
                ("page", page_num),
                # 100 is the max return size of the API.
                ("pageSize", 100),
                ("txDate", "all"),
                ("politician", politician_id)
            )
            r = self.__session.get(
                self.__url + "/trades",
                headers=self.__get_headers(),
                params=params,
            )
            r.raise_for_status()

            response_json = r.json()
            data = response_json["data"]
            all_trades.extend(data)

            if len(all_trades) >= response_json["meta"]["paging"]["totalItems"] or not data:
                paginating = False
            else:
                page_num += 1

        return all_trades

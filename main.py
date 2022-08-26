from dateutil.parser import parse
from datetime import datetime as dt, timedelta
import dotenv
import logging
import os
from typing import Any, Dict, Optional, Tuple

from pushbullet import Pushbullet

from capitoltrades import CapitolTrades

class Parsers:

    @staticmethod
    def tx_date(indate: str = ""):
        days = (dt.now().date() - parse(indate).date()).days
        if days:
            return "%s (%s months)" % (indate, "{:.1f}".format(days/30))
        return ""

    @staticmethod
    def share_price(shareprice: str = None):
        if shareprice == None:
            return ""
        return "x $%s" % shareprice
    
    @staticmethod
    def presentable_trade(tx: Dict[str, Any], name: str) -> Tuple[str, str]:
        """Creates a presentable trade which can be consumed by the Pushbullet API."""
        title = "New 💰 by %s" % name
        body = """🏢: %s
        💰: %s
        📅: %s
        💸: %s
        #️⃣: %s %s
        💬: %s""" % (
            tx.get("asset", {}).get("assetTicker"),
            Parsers.tx_date(tx.get("txDate")), 
            tx.get("txType"), 
            tx.get("value"), 
            tx.get("size"), 
            Parsers.share_price(tx.get("price")),
            tx.get("comment")
        )
        return title, body


def _init_pb() -> Optional[Pushbullet]:
    api_key = os.getenv("PUSHBULLET_API_KEY")
    if not api_key:
        return None
    else:
        return Pushbullet(api_key)

def main(
    capitol: CapitolTrades,
    pb: Optional[Pushbullet],
    check_dates: bool = True,
    name: str = "Pelosi",
):
    """A quick script to grab all of a politician's trades.
    If check_date = True, only displays trades within the last three days,
    otherwise displays all trades."""
    nancy_id = capitol.get_politician_id(name)
    p = capitol.trades(nancy_id)

    for tx in p:
        if not tx:
            continue

        if check_dates:
            if any(
                date_checker(tx["pubDate"]) for date_checker in [
                    lambda d: parse(d).date() + timedelta(days=1) == dt.now().date(),
                    lambda d: parse(d).date() + timedelta(days=2) == dt.now().date(),
                    lambda d: parse(d).date()  == dt.now().date()
                ]
            ):
                title, body = Parsers.presentable_trade(tx, name)
                print(title, body, "\n") if not pb else pb.push_note(title, body)
        else:
            title, body = Parsers.presentable_trade(tx, name)
            print(title, body, "\n") if not pb else pb.push_note(title, body)
        
    print("Done fetching values.")

if __name__ == "__main__":
    logging.basicConfig(
        handlers=[
            logging.FileHandler("trades.log"),
            logging.StreamHandler()
        ],
        format="%(asctime)s %(message)s",
        datefmt="%H:%M:%S",
        level=logging.DEBUG
    )

    dotenv.load_dotenv(".env")

    capitol = CapitolTrades()
    pb = _init_pb()
    main(capitol, pb)

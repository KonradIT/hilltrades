from capitoltrades import CapitolTrades, PoliticalParty, CongressType
from pprint import pprint
from pushbullet import Pushbullet
import os
from dateutil.parser import parse
from datetime import datetime as dt
import logging
import dotenv
import time

logging.basicConfig(handlers=[
    logging.FileHandler("trades.log"),
    logging.StreamHandler()
],
    format="%(asctime)s %(message)s",
    datefmt="%H:%M:%S",
    level=logging.INFO)

dotenv.load_dotenv(".env")

assert os.getenv("PUSHBULLET_API_KEY") is not None
pb = Pushbullet(os.getenv("PUSHBULLET_API_KEY"))
capitol = CapitolTrades()


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


nancy = capitol.get_politician_id("Pelosi")
p = capitol.trades(
    politicians=[nancy],
    politicianParty=PoliticalParty.BOTH,
    congressType=CongressType.REPRESENTATIVE,
    ticker=True
)

for tx in p:

    if parse(tx.get("addedDate")).date() == dt.now().date():
        logging.info(str(tx))

        pb.push_note("New 💰 by Nancy Pelosi", """🏢: %s
💰: %s
📅: %s
💸: %s
#️⃣: %s %s
💬: %s""" % (tx.get("ticker"), Parsers.tx_date(tx.get("transactionDate")), tx.get("tradeType"), tx.get("tradeValueRange"), tx.get("shares"), Parsers.share_price(tx.get("sharePrice")), tx.get("comment")))
        time.sleep(2)

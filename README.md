# SignalsFromTheHill

Python wrapper around the CapitolTrades.com API. 

Examples will include:

- Send notifications to pushbullet whenever the 45 days pass since your favorite ~~insider trader~~ politician traded a stock.
- Sync up trades to Degiro

## Automation

`pm2 start notifier.config.js`

## Optional Flask Server
If not using Pushbullet, we also offer the option to run this Python wrapper as a stand-alone Flask app which can run on it's own server be queried as an API.

```
# To run the server on http://127.0.0.1:5000
$ FLASK_APP=app flask run
```

```
# Example requests and responses

# Step 1: Find the ID of the politician I am interested in using this hash map.
$ curl 127.0.0.1:5000/get-pids
{
    "A000148":"Auchincloss, Jacob Daniel (Jake)","A000360":"Alexander, Andrew Lamar, Jr","A000367":"Amash, Justin",
    "A000372":"Allen, Richard Wayne (Rick)","A000378":"Axne, Cynthia Lynne (Cindy)","B000574":"Blumenauer, Earl Francis","B000575":"Blunt, Roy Dean", 
    ... 
}

# Step 2: Find trades for "A000367":"Amash, Justin"
$ curl 127.0.0.1:5000/by-pid/A000367
[
    {
        "_assetId":100006760,
        "_issuerId":431303,
        "_politicianId":"A000367",
        "_txId":20000338178,
        "asset":
            {
                "assetTicker":"DIS:US","assetType":"stock",
                "instrument":null
            },
        "chamber":"house",
        "comment":"SUBHOLDING OF: Charles Schwab Investment Account - DC1",
        "committees":[],
        "filingDate":"2020-04-15",
        "filingId":200129308,
        "filingURL":"https://disclosures-clerk.house.gov/public_disc/ptr-pdfs/2020/20016417.pdf","hasCapitalGains":false,
        "issuer":
            {
                "_stateId":"ca",
                "c2iq":"JARVU1B0",
                "country":"us",
                "issuerName":"The Walt Disney Co","issuerTicker":"DIS:US","sector":"communication-services"
            },
        "labels":[],
        "owner":"child",
        "politician":
            {
                "_stateId":"mi",
                "chamber":"house",
                "dob":"1980-04-18",
                "firstName":"Justin",
                "gender":"male",
                "lastName":"Amash",
                "nickname":null,
                "party":"other"
            },
        "price":88.8,
        "pubDate":"2020-04-17T00:00:00Z","reportingGap":28,
        "size":367,
        "sizeRangeHigh":564,
        "sizeRangeLow":169,
        "txDate":"2020-03-18",
        "txType":"buy",
        "txTypeExtended":null,
        "value":32500
    },
    ...
]
```

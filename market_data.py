import yfinance as yf

FX_TICKERS = {

"MXN": "MXN=X",
"BRL": "BRL=X",
"COP": "COP=X",
"PEN": "PEN=X",
"CLP": "CLP=X",
"ARS": "ARS=X",
"UYU": "UYU=X",
"CRC": "CRC=X"

}

ENERGY_TICKERS = {

"BRENT": "BZ=F",
"WTI": "CL=F",
"NATGAS": "NG=F",
"GASOLINE": "RB=F"

}

GLOBAL_TICKERS = {

"SP500": "^GSPC",
"NASDAQ": "^IXIC",
"DOW": "^DJI",
"DAX": "^GDAXI",
"NIKKEI": "^N225",

"GOLD": "GC=F",
"SILVER": "SI=F",

"BITCOIN": "BTC-USD",
"ETHEREUM": "ETH-USD"

}

def get_price(ticker):

    data = yf.Ticker(ticker)

    hist = data.history(period="2d")

    if len(hist) < 2:
        return None

    today = hist["Close"].iloc[-1]
    yesterday = hist["Close"].iloc[-2]

    change = today - yesterday
    pct = (change / yesterday) * 100

    return round(today,2), round(pct,2)

def get_assets_data(assets):

    results = {}

    for asset in assets:

        ticker = None

        if asset in FX_TICKERS:
            ticker = FX_TICKERS[asset]

        elif asset in ENERGY_TICKERS:
            ticker = ENERGY_TICKERS[asset]

        elif asset in GLOBAL_TICKERS:
            ticker = GLOBAL_TICKERS[asset]

        if ticker:

            data = get_price(ticker)

            if data:

                price, pct = data

                results[asset] = {

                    "price": price,
                    "change": pct

                }

    return results


def get_top_movers():

    assets = []

    assets += list(FX_TICKERS.keys())
    assets += list(ENERGY_TICKERS.keys())
    assets += list(GLOBAL_TICKERS.keys())

    data = get_assets_data(assets)

    movers = []

    for asset in data:

        movers.append((asset, data[asset]["change"]))

    movers.sort(key=lambda x: abs(x[1]), reverse=True)

    return movers[:5]
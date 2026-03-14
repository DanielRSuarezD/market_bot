import yfinance as yf


TICKERS = {

# ENERGY
"BRENT":"BZ=F",
"WTI":"CL=F",

# METALS
"GOLD":"GC=F",
"SILVER":"SI=F",

# FX LATAM
"MXN":"MXN=X",
"BRL":"BRL=X",
"COP":"COP=X",
"PEN":"PEN=X",
"CLP":"CLP=X",
"ARS":"ARS=X",
"UYU":"UYU=X",
"CRC":"CRC=X",
"GTQ":"GTQ=X",
"BOB":"BOB=X",
"PYG":"PYG=X",

# FX GLOBAL
"EUR":"EURUSD=X",
"GBP":"GBPUSD=X",
"CHF":"CHF=X",
"JPY":"JPY=X",
"RUB":"RUB=X",
"AED":"AED=X",

# INDICES
"SP500":"^GSPC",
"NASDAQ":"^IXIC",

# DOLLAR INDEX
"DXY":"DX-Y.NYB"

}


FLAGS = {

"MXN":"🇲🇽",
"BRL":"🇧🇷",
"COP":"🇨🇴",
"PEN":"🇵🇪",
"CLP":"🇨🇱",
"ARS":"🇦🇷",
"UYU":"🇺🇾",
"CRC":"🇨🇷",
"GTQ":"🇬🇹",
"BOB":"🇧🇴",
"PYG":"🇵🇾",

"EUR":"🇪🇺",
"GBP":"🇬🇧",
"CHF":"🇨🇭",
"JPY":"🇯🇵",
"RUB":"🇷🇺",
"AED":"🇦🇪"

}


def get_price(symbol):

    ticker = yf.Ticker(symbol)

    data = ticker.history(period="1d")

    close = data["Close"].iloc[-1]
    openp = data["Open"].iloc[-1]

    change = ((close-openp)/openp)*100

    return round(close,2), round(change,2)


def get_market():

    text="🌍 MARKET MONITOR\n\n"

# ENERGY
    text+="🛢 ENERGY\n"

    for asset in ["BRENT","WTI"]:

        price,change=get_price(TICKERS[asset])

        dot="🔴" if change<0 else "🟢"

        text+=f"{asset}: {price} {dot} ({change}%)\n"

    text+="\n"

# METALS
    text+="🥇 METALS\n"

    for asset in ["GOLD","SILVER"]:

        price,change=get_price(TICKERS[asset])

        dot="🔴" if change<0 else "🟢"

        text+=f"{asset}: {price} {dot} ({change}%)\n"

    text+="\n"

# FX
    text+="💱 FX MARKETS\n"

    for asset in ["EUR","MXN","COP","PEN","CRC","RUB"]:

        price,change=get_price(TICKERS[asset])

        flag=FLAGS.get(asset,"")

        dot="🔴" if change<0 else "🟢"

        text+=f"{flag} {asset}: {price} {dot} ({change}%)\n"

    text+="\n"

# DOLLAR INDEX
    price,change=get_price(TICKERS["DXY"])

    dot="🔴" if change<0 else "🟢"

    text+="💵 DOLLAR INDEX\n"
    text+=f"DXY: {price} {dot} ({change}%)\n"

    return text

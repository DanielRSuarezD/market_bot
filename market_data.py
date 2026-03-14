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

"MXN":"🇲🇽","BRL":"🇧🇷","COP":"🇨🇴","PEN":"🇵🇪",
"CLP":"🇨🇱","ARS":"🇦🇷","UYU":"🇺🇾","CRC":"🇨🇷",
"GTQ":"🇬🇹","BOB":"🇧🇴","PYG":"🇵🇾",

"EUR":"🇪🇺","GBP":"🇬🇧","CHF":"🇨🇭",
"JPY":"🇯🇵","RUB":"🇷🇺","AED":"🇦🇪"
}


def get_price(symbol):

    ticker = yf.Ticker(symbol)

    data = ticker.history(period="1d")

    close = data["Close"].iloc[-1]
    openp = data["Open"].iloc[-1]

    change = ((close-openp)/openp)*100

    return round(close,2), round(change,2)


def build_line(asset):

    price,change = get_price(TICKERS[asset])

    flag = FLAGS.get(asset,"")

    dot = "🟢" if change >= 0 else "🔴"

    return f"{flag} {asset}: {price} {dot} ({change}%)\n"


def get_market(user_assets):

    text="🌍 MARKET MONITOR\n\n"


# ENERGY
    energy = [a for a in user_assets if a in ["BRENT","WTI"]]

    if energy:
        text+="🛢 ENERGY\n"
        for a in energy:
            text+=build_line(a)
        text+="\n"


# METALS
    metals = [a for a in user_assets if a in ["GOLD","SILVER"]]

    if metals:
        text+="🥇 METALS\n"
        for a in metals:
            text+=build_line(a)
        text+="\n"


# FX
    fx = [a for a in user_assets if a in FLAGS]

    if fx:
        text+="💱 FX MARKETS\n"
        for a in fx:
            text+=build_line(a)
        text+="\n"


# INDICES
    idx = [a for a in user_assets if a in ["SP500","NASDAQ"]]

    if idx:
        text+="📈 INDICES\n"
        for a in idx:
            text+=build_line(a)
        text+="\n"


# DXY
    price,change=get_price(TICKERS["DXY"])

    dot="🟢" if change>=0 else "🔴"

    text+="💵 DOLLAR INDEX\n"
    text+=f"DXY: {price} {dot} ({change}%)\n"

    return text

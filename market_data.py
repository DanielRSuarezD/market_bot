import requests
import yfinance as yf


def get_fx():

    url = "https://open.er-api.com/v6/latest/USD"

    r = requests.get(url)

    data = r.json()

    rates = data["rates"]

    fx = {}

    fx["EUR"] = round(1 / rates["EUR"], 3)
    fx["MXN"] = round(rates["MXN"], 2)
    fx["COP"] = round(rates["COP"], 2)
    fx["PEN"] = round(rates["PEN"], 2)
    fx["CRC"] = round(rates["CRC"], 2)
    fx["RUB"] = round(rates["RUB"], 2)
    fx["AED"] = round(rates["AED"], 2)

    return fx

def get_oil():

    brent = yf.Ticker("BZ=F").history(period="1d")["Close"].iloc[-1]
    wti = yf.Ticker("CL=F").history(period="1d")["Close"].iloc[-1]

    urals = brent - 15

    return {
        "Brent": round(float(brent),2),
        "WTI": round(float(wti),2),
        "Urals": round(float(urals),2),
        "Spread": round(float(brent-urals),2)
    }


def get_dxy():

    dxy = yf.Ticker("DX-Y.NYB").history(period="1d")["Close"].iloc[-1]

    return round(float(dxy),2)


import yfinance as yf

def get_global():

    data = {}

    data["SP500"] = round(yf.Ticker("^GSPC").history(period="1d")["Close"].iloc[-1],2)

    data["Gold"] = round(yf.Ticker("GC=F").history(period="1d")["Close"].iloc[-1],2)

    data["Silver"] = round(yf.Ticker("SI=F").history(period="1d")["Close"].iloc[-1],2)

    data["BTC"] = round(yf.Ticker("BTC-USD").history(period="1d")["Close"].iloc[-1],2)

    return data

def get_history(symbol):

    ticker = f"{symbol}=X"

    data = yf.Ticker(ticker).history(period="7d")["Close"]

    return data
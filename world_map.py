import geopandas as gpd
import matplotlib.pyplot as plt
import yfinance as yf
import requests
import zipfile
import os


def get_market_change(ticker):

    data = yf.Ticker(ticker).history(period="2d")["Close"]

    if len(data) < 2:
        return 0

    return (data.iloc[-1] - data.iloc[-2]) / data.iloc[-2] * 100


def download_world():

    url = "https://naturalearth.s3.amazonaws.com/110m_cultural/ne_110m_admin_0_countries.zip"

    if not os.path.exists("world.zip"):

        r = requests.get(url)

        with open("world.zip", "wb") as f:
            f.write(r.content)

        with zipfile.ZipFile("world.zip", "r") as zip_ref:
            zip_ref.extractall("world")


def generate_world_map():

    download_world()

    world = gpd.read_file("world/ne_110m_admin_0_countries.shp")

    markets = {
        "North America": get_market_change("^GSPC"),
        "Europe": get_market_change("^STOXX50E"),
        "Asia": get_market_change("^N225"),
        "South America": get_market_change("^BVSP")
    }

    world["market"] = world["CONTINENT"].map(markets)

    plt.figure(figsize=(12,6))

    world.plot(
        column="market",
        cmap="RdYlGn",
        legend=True,
        missing_kwds={"color":"lightgrey"}
    )

    plt.title("Global Market Map")

    file = "world_market_map.png"

    plt.savefig(file)

    plt.close()

    return file
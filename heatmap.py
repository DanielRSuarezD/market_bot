import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

from market_data import get_fx, get_oil, get_dxy, get_global


def generate_heatmap():

    fx = get_fx()
    oil = get_oil()
    dxy = get_dxy()
    global_m = get_global()

    data = {
        "S&P500": global_m["SP500"],
        "Gold": global_m["Gold"],
        "Bitcoin": global_m["BTC"],
        "Brent": oil["Brent"],
        "WTI": oil["WTI"],
        "DXY": dxy,
        "EUR": fx["EUR"],
        "MXN": fx["MXN"],
        "COP": fx["COP"]
    }

    df = pd.DataFrame(list(data.items()), columns=["Market","Value"])

    df["Normalized"] = (df["Value"] - df["Value"].mean()) / df["Value"].std()

    pivot = df.pivot_table(values="Normalized", index="Market")

    plt.figure(figsize=(6,6))

    sns.heatmap(
        pivot,
        cmap="RdYlGn",
        center=0,
        annot=True
    )

    plt.title("Global Market Heatmap")

    file = "heatmap.png"

    plt.savefig(file)

    plt.close()

    return file
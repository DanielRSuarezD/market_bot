import matplotlib.pyplot as plt
from market_data import get_history


def generate_chart(symbol):

    data = get_history(symbol)

    plt.figure(figsize=(6,4))

    plt.plot(data.index, data.values)

    plt.title(f"{symbol} Weekly Trend")
    plt.xlabel("Date")
    plt.ylabel("Price")

    file = f"{symbol}_chart.png"

    plt.savefig(file)

    plt.close()

    return file
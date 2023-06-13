from time import sleep
from pybit.unified_trading import HTTP

session = HTTP(
    testnet=False,
)


def get_volume(symbol):
    turnover = "0"
    ticker = session.get_tickers(category="spot", symbol=symbol)
    if ticker["retMsg"] == "OK":
        result = ticker["result"]
        if "list" in result:
            data = result["list"][0]
            turnover = int(data["turnover24h"].split(".")[0])

    return turnover


def main():
    instruments = session.get_instruments_info(category="spot")
    tokens = []

    if instruments["retMsg"] == "OK":
        result = instruments["result"]
        if "list" in result:
            data = result["list"]
            for index, row in enumerate(data):
                symbol = row["symbol"]
                status = row["status"]

                if status.upper() == "TRADING":
                    volume = get_volume(symbol)
                    tokens.append((symbol, volume))
                    print(f"{index}/{len(data)} ")
                    sleep(1)

        tokens = sorted(tokens, key=lambda x: x[1], reverse=True)

    else:
        raise Exception("Invalid instruments")

    for token in tokens:
        print(f"{token[0]}: {token[1]} $")

    with open("tokens.txt", "w") as f:
        for token in tokens:
            f.write(f"{token[0]}: {token[1]} $\n")


if __name__ == "__main__":
    main()

import sys
import signal
import argparse
from time import sleep, time

from pybit.unified_trading import WebSocket

from models.trade import SpotTradeBybit
from services.logger import Logger
from services.database import Database

ws = WebSocket(testnet=False, channel_type="spot")


def shutdown_handler(signum, frame):
    # Perform any cleanup tasks here
    logger.info("Shutting down...")
    ws.exit()
    sys.exit(0)


def handle_trade(message):
    rx_ts = int(time() * 1000)
    trade = SpotTradeBybit(**message)
    global_ts = trade.ts

    logger.log_trade(
        global_ts,
        trade.data.S,
        trade.data.s,
        trade.data.v,
        trade.data.p,
        "AGGREGATE" if trade.trades_count > 1 else "SINGLE",
    )

    logger.debug(f"latency: {rx_ts-global_ts} ms trade_count: {trade.trades_count}")
    db.add_bybit_spot_trade(trade, rx_ts)


def main(args):
    global db
    global logger
    logger = Logger(f"bybit_spot_{args.symbol.upper()}")
    try:
        db = Database(server=args.server, symbol=args.symbol.upper())

        # Shutdown server gracefully to close all connections and minimize hanging connections
        signal.signal(signal.SIGINT, shutdown_handler)

        ws.trade_stream(symbol=args.symbol.upper(), callback=handle_trade)

        while True:
            sleep(1)
    except Exception as e:
        logger.error(e)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Bybit Spot Trade Stream")
    # Add arguments
    parser.add_argument("--symbol", type=str, help="Symbol to subscribe")
    parser.add_argument("--server", type=str, help="Server name")
    args = parser.parse_args()

    main(args)

import os
import sys
import math
import signal
import cProfile
import argparse
from time import sleep, time, perf_counter

from pybit.unified_trading import WebSocket

from models.trade import SpotTradeBybit
from models.bybit_symbols import all_symbols
from models.db import BYBIT_TRADE

from services.logger import Logger
from services.database import Database
from services.metrics import Metrics


ws = WebSocket(testnet=False, channel_type="spot")

ENV = os.environ.get("ENV", None)
MAX_SYMBOLS = 50


def shutdown_handler(signum, frame):
    # Perform any cleanup tasks here
    logger.info("Shutting down...")
    if ENV and ENV == "development":
        if profiler:
            profiler.disable()
            profiler.print_stats()

    ws.exit()
    db.close()
    sys.exit(0)


def handle_trade(message):
    # Used for profiling this function
    func_start_time = perf_counter()

    metrics.increase()

    trade = SpotTradeBybit(**message)

    # Time when message was dispatched from server
    tx_ts = trade.ts
    # Time when message was received
    rx_ts = int(time() * 1000)

    logger.log_trade(
        tx_ts,
        trade.data.S,
        trade.data.s,
        trade.data.v,
        trade.data.p,
        "AGGREGATE" if trade.trades_count > 1 else "SINGLE",
    )

    db.add_bybit_spot_trade(trade, rx_ts)

    # Used for profiling this function
    func_end_time = perf_counter()

    latency = rx_ts - tx_ts
    execution_time = func_end_time - func_start_time

    logger.debug(
        f"latency: {latency} ms execution: {(execution_time):.6f} ms mps: {metrics.message_rate} trade_count: {trade.trades_count}"
    )


def main(args):
    global db
    global logger
    global metrics

    logger = Logger("bybit_spot_trades")

    metrics = Metrics()

    # Understanding how much this client can handle
    if ENV and ENV == "development":
        global profiler

        profiler = cProfile.Profile()
        profiler.enable()

    try:
        db = Database(server=args.server, entity_type=BYBIT_TRADE)

        # Shutdown server gracefully to close all connections and minimize hanging connections
        signal.signal(signal.SIGINT, shutdown_handler)

        # Currently we handle 10 symbols per ws connection and single ws connection per application.
        # So we need a way to index which client will be running which symbols.
        # This is achieved by using cli argument - index
        client_ix = args.index
        symbols_start = 0 if client_ix == 0 else 10 * client_ix
        symbols_end = 10 if client_ix == 0 else 10 * (client_ix + 1)

        if symbols_end > len(all_symbols):
            symbols_end = len(all_symbols)

        symbols = all_symbols[symbols_start:symbols_end]

        ws.trade_stream(symbol=symbols, callback=handle_trade)

        while True:
            sleep(1)
    except Exception as e:
        logger.error(e)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Bybit Spot Trade Stream")

    parser.add_argument("--index", type=int, help="Bot index", default=0)
    parser.add_argument("--server", type=str, help="Server name", default="default")
    args = parser.parse_args()

    main(args)

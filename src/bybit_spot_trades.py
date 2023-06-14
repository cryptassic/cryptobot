import os
import sys
import math
import signal
import argparse
from time import sleep, time, perf_counter

from pybit.unified_trading import WebSocket

from models.trade import SpotTradeBybit
from models.bybit_symbols import SYMBOLS
from services.logger import Logger
from services.database import Database
from services.metrics import Metrics

import cProfile

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

    # for conn in ws_connections:
    # conn.exit()
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


def init_connections():
    connections = []
    # We can only subscribe to 10 symbols per connection

    total_symbols = len(SYMBOLS[:MAX_SYMBOLS])

    conn_required = math.ceil(total_symbols / 10)

    symbol_start_slice = 0
    symbol_end_slice = 10

    for _ in range(0, conn_required):
        ws = WebSocket(testnet=False, channel_type="spot")
        ws_symbols = SYMBOLS[symbol_start_slice:symbol_end_slice]

        ws.trade_stream(symbol=ws_symbols, callback=handle_trade)

        connections.append(ws)

        symbol_start_slice = symbol_end_slice
        symbol_end_slice += 10

    return connections


def main(args):
    global db
    global logger
    global metrics
    global ws_connections
    logger = Logger("bybit_spot_trades")

    metrics = Metrics()

    # Understanding how much this client can handle
    if ENV and ENV == "development":
        global profiler

        profiler = cProfile.Profile()
        profiler.enable()

    try:
        db = Database(server=args.server, symbol=args.symbol.upper())

        # Shutdown server gracefully to close all connections and minimize hanging connections
        signal.signal(signal.SIGINT, shutdown_handler)

        # ws_connections = init_connections()
        # ws.trade_stream(symbol=args.symbol.upper(), callback=handle_trade)
        ws.trade_stream(symbol=SYMBOLS[:10], callback=handle_trade)

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

import os
import sys
import signal
import cProfile

from typing import List
from time import perf_counter, time
from pybit.unified_trading import WebSocket

from services.logger import Logger
from services.database import Database
from services.metrics import Metrics

from models.trade import SpotTradeBybit
from models.bybit_symbols import get_symbols


ENV = os.environ.get("ENV", None)


class Client:
    db: Database
    ws: WebSocket
    metrics: Metrics
    symbols: List[str]
    profiler: cProfile.Profile
    logger: Logger

    def __init__(
        self,
        server: str,
        instrument_type: str,
        index: int,
    ):
        self.__start_profiler()
        self.instrument_type = instrument_type

        self.logger = Logger.getLogger("application")
        self.metrics = Metrics()

        self.__load_symbols(index)

        self.db = Database(server=server)
        self.ws = WebSocket(testnet=False, channel_type=instrument_type.lower())

        # Shutdown server gracefully to close all connections and minimize hanging connections
        signal.signal(signal.SIGINT, self.__shutdown_handler)

    def __shutdown_handler(self, *args):
        # Perform any cleanup tasks here
        self.logger.info("Shutting down...")

        if ENV and ENV == "development":
            if self.profiler:
                self.profiler.disable()
                self.profiler.print_stats()

        self.ws.exit()
        self.db.close()
        sys.exit(0)

    def __start_profiler(self):
        # Understanding how much this client can handle
        if ENV and ENV == "development":
            self.profiler = cProfile.Profile()
            self.profiler.enable()

    def __load_symbols(self, index: int):
        # Currently we handle 10 symbols per ws connection and single ws connection per application.
        # So we need a way to index which client will be running which symbols.
        # This is achieved by using cli argument - index
        client_ix = index
        symbols_start = 0 if client_ix == 0 else 10 * client_ix
        symbols_end = 10 if client_ix == 0 else 10 * (client_ix + 1)

        all_symbols = get_symbols(self.instrument_type)

        if symbols_end > len(all_symbols):
            symbols_end = len(all_symbols)

        assert (
            symbols_start <= symbols_end
        ), f"Failed to load symbols. \
        Check client index or {self.instrument_type.upper()} symbols. \
        Client tries to get more symbols that there are available"

        self.symbols = all_symbols[symbols_start:symbols_end]


class Bybit(Client):
    def __init__(self, *args, **kwargs):
        """
        Constructor for Trades client.

        Parameters:
        -----------
            - `server` (str) : Server name where client is running
            - `instrument_type` (str) : SPOT or PERP
            - `index` (int) : Client index used to distribute tasks

        """
        super().__init__(*args, **kwargs)

    def __handle_trade(self, message):
        # Used for profiling this function
        func_start_time = perf_counter()

        self.metrics.increase()

        trade = SpotTradeBybit(**message)

        # Time when message was dispatched from server
        tx_ts = trade.ts
        # Time when message was received
        rx_ts = int(time() * 1000)

        self.logger.log_trade(
            tx_ts,
            trade.data.S,
            trade.data.s,
            trade.data.v,
            trade.data.p,
            "AGGREGATE" if trade.trades_count > 1 else "SINGLE",
        )

        self.db.add_bybit_spot_trade(trade, rx_ts)

        # Used for profiling this function
        func_end_time = perf_counter()

        latency = rx_ts - tx_ts
        execution_time = func_end_time - func_start_time

        self.logger.debug(
            f"latency: {latency} ms execution: {(execution_time):.6f} ms mps: {self.metrics.message_rate} trade_count: {trade.trades_count}"
        )

    def __handle_orderbook(self, message):
        pass

    def subscribe_trades(self):
        if self.__can_subscribe():
            self.ws.trade_stream(symbol=self.symbols, callback=self.__handle_trade)

    def subscribe_orderbook(self, depth=50):
        if self.__can_subscribe():
            self.ws.orderbook_stream(
                depth=depth, symbol=self.symbols, callback=self.__handle_orderbook
            )

    def __can_subscribe(self) -> bool:
        if not self.ws:
            self.logger.error("Websocket not connected")
            return False
        elif not self.symbols or len(self.symbols) == 0:
            self.logger.error("No symbols to subscribe to")
            return False

        return True

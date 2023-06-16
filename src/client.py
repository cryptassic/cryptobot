import os
import sys
import signal
import cProfile

from typing import List
from pprint import pprint
from time import perf_counter, time
from pybit.unified_trading import WebSocket

from services.logger import Logger
from services.database import Database
from services.metrics import Metrics
from services.orderbook import BookKeeper

from models.trade import SpotTradeBybit
from models.bybit_symbols import get_symbols
from models.db import ExchangeDataEntityType


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
        entity_type: ExchangeDataEntityType,
    ):
        self.__start_profiler()
        self.instrument_type = instrument_type

        self.logger = Logger.getLogger("application")
        self.metrics = Metrics()

        self.__load_symbols(index)

        self.db = Database(server=server, entity_type=entity_type)
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
        # For debugging purposes we only load single symbol
        if index == -1:
            self.symbols = [get_symbols(self.instrument_type)[0]]
            return

        # Another for debugging purposes ;)
        elif index == -69:
            self.symbols = get_symbols(self.instrument_type)[:3]
            return

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
            - `entity_type` (ExchangeDataEntityType) : Data type

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
        # Used for profiling this function
        func_start_time = perf_counter()

        # Time when message was received
        rx_ts = int(time() * 1000)

        if message and message["type"] == "snapshot" or message["data"]["u"] == 1:
            # Storing all messages in buffer with time window of 1 second.
            # This allows us to reduce noise and save some storage space in database.
            #
            # Normally orderbook data is pushed 10/second.
            # So, we reduce to only 1/second by aggregating all messages in buffer.

            symbol = message["topic"].split(".")[-1]

            # Orderbook is where we keep marketdepth. It is singleton so no new instances are created.
            orderbook = BookKeeper.get_instance(symbol)

            # We simply add messages to the buffer from where orderbook.get() method returns accumulated results.
            # Keep in mind that if buffer is empty or interval window is not passed, then result will be None.
            orderbook.update(message)

            # We try to get a aggregated object from the buffer. We will get None if buffer is empty or interval window is not passed.
            c_depth = orderbook.get()

            # Used for profiling this function

            if c_depth:
                func_end_time = perf_counter()

                latency = rx_ts - message["ts"]

                self.db.add_bybit_spot_orderbook(c_depth, rx_ts)

                self.logger.debug(
                    f"{symbol}  bid: [{c_depth.data.b[0].size}]{c_depth.data.b[0].price}/{c_depth.data.a[0].price}[{c_depth.data.a[0].size}] : ask execution: {func_end_time-func_start_time:.6f} ms latency: {latency} ms"
                )

                # self.logger.debug(
                #     f"[{c_depth.data.b[0].size}]{c_depth.data.b[0].price}/{c_depth.data.a[0].price}[{c_depth.data.a[0].size}]"
                # )

            # else:
            #     # self.logger.debug(
            #     #     f"Buffer size: {len(orderbook.buffer.buffer)} bid: {message['data']['b'][0][0]}/{message['data']['a'][0][0]} :ask"
            #     # )
            #     bid = message["data"]["b"][0]
            #     ask = message["data"]["a"][0]
            #     self.logger.debug(f"[{bid[1]}]{bid[0]}/{ask[0]}[{ask[1]}]")
            return
        else:
            self.logger.error(
                f"finnaly delta received {message}. Don't know how to handle this"
            )

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

import os
import pytz
import datetime

# import time as perf_time

import psycopg2
from psycopg2.extras import execute_values

from models.marketdepth import MarketDepth

from .logger import Logger

from models.trade import SpotTradeBybit
from models.db import ExchangeDataEntityType

USER = os.environ.get("DB_USER", None)
PASSWORD = os.environ.get("DB_PASSWORD", None)
ENV = os.environ.get("ENV", None)

# MAX_BATCH_SIZE = 100
MAX_BATCH_SIZE = int(os.environ.get("DB_BATCH_SIZE", 100))

# DB_TRADES_TABLE = "bybit_spot_trade" if ENV == "production" else "test_table_trade"
# DB_ORDERBOOK_TABLE = (
#     "bybit_spot_orderbook" if ENV == "production" else "test_table_orderbook"
# )


class Database:
    def __init__(self, server: str, entity_type: ExchangeDataEntityType):
        self.batch = []
        self.server = server
        self.logger = Logger("db")

        self.DB_TABLE = (
            entity_type.value[0]
            if ENV == "production"
            else "test_" + entity_type.value[0]
        )
        self.TABLE_COLUMNS = entity_type.value[1]

        if USER and PASSWORD:
            self.connection = psycopg2.connect(
                user=USER,
                password=PASSWORD,
                host="nc7hjuhxja.pb9ebh0mza.tsdb.cloud.timescale.com",
                port="33076",
                database="tsdb",
            )
        else:
            raise Exception("DB_USER or DB_PASSWORD is not set")

    def get_cursor(self):
        return self.connection.cursor()

    def add_bybit_spot_trade(self, trade: SpotTradeBybit, data_recv_ts: int):
        time = self._get_timestamptz(trade.ts)
        trade_id = trade.data.i
        trade_type = "AGGREGATE" if trade.trades_count > 1 else "SINGLE"
        trade_fill_time = self._get_timestamptz(trade.data.T)
        trade_side = trade.data.S
        trade_symbol = trade.data.s
        trade_qty = trade.data.v
        trade_price = trade.data.p
        trades_count = trade.trades_count
        block_trade = trade.data.BT
        exchange = "BYBIT"
        rx_time = self._get_timestamptz(data_recv_ts)
        latency = data_recv_ts - trade.ts

        data = (
            time,
            trade_id,
            trade_type,
            trade_fill_time,
            trade_side,
            trade_symbol,
            trade_qty,
            trade_price,
            trades_count,
            block_trade,
            self.server,
            exchange,
            rx_time,
            latency,
        )

        if len(self.batch) >= MAX_BATCH_SIZE:
            self.__execute_batch()
            self.batch = []
            self.logger.info(f"INSERT {MAX_BATCH_SIZE} BATCH")

        self.batch.append(data)

    def add_bybit_spot_orderbook(self, depth: MarketDepth, data_recv_ts: int):
        time = self._get_timestamptz(depth.ts)
        update_id = depth.data.u
        seq = depth.data.seq
        book_symbol = depth.topic.split(".")[-1].upper()

        # Default ask1-50
        # Thats why we need to reverse the sequence to be ask50-1
        asks = tuple(val for obj in depth.data.a[::-1] for val in (obj.price, obj.size))
        # Sometimes marketdepth is very shallow, so we need to fill it with default values of 0.
        # Default element lenght is 100, but sometimes we get like 73 or smth...
        asks = (("0",) * (100 - len(asks))) + asks

        # bid1-50
        bids = tuple(val for obj in depth.data.b for val in (obj.price, obj.size))
        # Same for bid
        bids = bids + ("0",) * (100 - len(bids))

        assert len(asks) == len(bids) and len(asks) == 100, "Bid and Ask mismatch"

        server = self.server
        exchange = "BYBIT"
        rx_time = self._get_timestamptz(data_recv_ts)
        latency = data_recv_ts - depth.ts

        data = (
            (time, update_id, seq)
            + asks
            + bids
            + (book_symbol, server, exchange, rx_time, latency)
        )

        if len(self.batch) >= MAX_BATCH_SIZE:
            self.__execute_batch()
            self.batch = []
            self.logger.info(f"INSERT {MAX_BATCH_SIZE} BATCH")

        self.batch.append(data)

    def close(self):
        try:
            if not self.connection.closed:
                self.logger.info("Closed database connection")
                self.connection.close()
        except Exception as e:
            self.logger.error(e)

    def _get_timestamptz(self, timestamp):
        return (
            datetime.datetime.utcfromtimestamp(timestamp / 1000)
            .replace(tzinfo=pytz.utc)
            .strftime("%Y-%m-%d %H:%M:%S.%f %z")
        )

    def __execute_batch(self):
        cursor = self.get_cursor()

        sql = f"""
        INSERT INTO {self.DB_TABLE} ({','.join(self.TABLE_COLUMNS)})
        VALUES %s;"""

        try:
            execute_values(cursor, sql, self.batch)
            self.connection.commit()
        except Exception as e:
            # If an error occurs, the transaction is rolled back.
            self.connection.rollback()
            self.logger.error(f"{e}")

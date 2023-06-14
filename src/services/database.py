import os
import datetime
import pytz
import time as perf_time

import psycopg2
from psycopg2.extras import execute_values

from .logger import Logger

from models.trade import SpotTradeBybit
from models.db import SPOT_TRADE_BYBIT_COLUMNS

USER = os.environ.get("DB_USER", None)
PASSWORD = os.environ.get("DB_PASSWORD", None)
ENV = os.environ.get("ENV", None)

MAX_BATCH_SIZE = 100
DB_TABLE = "bybit_spot_trade" if ENV == "production" else "test_table"


class Database:
    def __init__(self, server: str):
        self.batch = []
        self.server = server
        self.logger = Logger("db")
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
        INSERT INTO {DB_TABLE} ({','.join(SPOT_TRADE_BYBIT_COLUMNS)}) 
        VALUES %s;"""

        try:
            execute_values(cursor, sql, self.batch)
            self.connection.commit()
        except Exception as e:
            # If an error occurs, the transaction is rolled back.
            self.connection.rollback()
            self.logger.error(f"{e}")

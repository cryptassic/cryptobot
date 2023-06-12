from typing import List
from dataclasses import dataclass


@dataclass
class SpotTradeDataBybit:
    i: str  # Trade id
    T: int  # Order fill time
    p: str  # Trade price
    v: str  # Trade size
    S: str  # Side of taker
    s: str  # Symbol name
    BT: bool  # Whether it is a block trade or not


@dataclass
class SpotTradeBybit:
    topic: str
    type: str
    ts: int
    data: SpotTradeDataBybit
    trades_count: int

    def __init__(self, **kwargs):
        self.topic = kwargs.get("topic", None)
        self.type = kwargs.get("type", None)
        self.ts = kwargs.get("ts", None)

        data = kwargs.get("data", None)
        if data:
            self.trades_count = len(data)
            self.data = self.aggregate_trades(data)
        else:
            self.trades_count = 0

    # Sometimes we receive multiple transactions, so we need to aggregate them to a single transaction
    def aggregate_trades(self, data) -> SpotTradeDataBybit:
        total_buy = 0
        total_sell = 0
        trade_symbol = ""
        latest_price = ""
        latest_fill_time = 0
        latest_BT = False
        latest_trade_id = 0

        for trade_args in data:
            aggr_trade = SpotTradeDataBybit(**trade_args)

            trade_id = int(aggr_trade.i)

            if trade_id > latest_trade_id:
                latest_trade_id = trade_id
                latest_price = aggr_trade.p
                latest_fill_time = aggr_trade.T
                latest_BT = aggr_trade.BT
                trade_symbol = aggr_trade.s

            if aggr_trade.S == "Buy":
                total_buy += float(aggr_trade.v)
            else:
                total_sell += float(aggr_trade.v)

        aggr_trade = SpotTradeDataBybit(
            i=str(trade_id),
            T=latest_fill_time,
            p=latest_price,
            v=str(abs((total_buy - total_sell))),
            S="Buy" if total_buy >= total_sell else "Sell",
            s=trade_symbol,
            BT=latest_BT,
        )

        return aggr_trade

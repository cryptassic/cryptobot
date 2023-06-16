from enum import Enum
from typing import List
from dataclasses import dataclass


class EntryType(Enum):
    BID = "bid"
    ASK = "ask"


@dataclass
class MarketDepthEntry:
    type: EntryType
    level: int
    price: str
    size: str


@dataclass
class MarketDepthData:
    s: str  # Symbol name
    b: List[MarketDepthEntry]  # Bids. Sorted by price in descending order
    a: List[MarketDepthEntry]  # Asks. Sorted by price in asceding order
    u: int  # Update ID
    seq: int  # Cross Sequence Number

    def __init__(self, **kwargs):
        self.s = kwargs.get("s", None)
        self.u = kwargs.get("u", None)
        self.seq = kwargs.get("seq", None)

        self.b = []
        self.a = []

        bids = kwargs.get("b", None)
        asks = kwargs.get("a", None)

        if bids and asks:
            asks = sorted(asks, key=lambda x: float(x[0]))
            bids = sorted(bids, key=lambda x: float(x[0]), reverse=True)

            for ix, (bid, ask) in enumerate(zip(bids, asks)):
                bid_entry = MarketDepthEntry(
                    type="bid", level=ix, price=bid[0], size=bid[1]
                )
                ask_entry = MarketDepthEntry(
                    type="ask", level=ix, price=ask[0], size=ask[1]
                )

                self.b.append(bid_entry)
                self.a.append(ask_entry)

            return
        else:
            raise TypeError(
                f"Unexpected empty bids or asks data received when parsing message to MarketDeptData object. message: {kwargs}"
            )


@dataclass
class MarketDepth:
    topic: str  # Topic name
    type: str  # Snapshot or Delta
    ts: int  # The timestamp (ms) that the system generates the data
    data: MarketDepthData

    def __init__(self, **kwargs):
        self.topic = kwargs.get("topic", None)
        self.type = kwargs.get("type", None)
        self.ts = kwargs.get("ts", None)

        data = kwargs.get("data", None)

        if data:
            depth = MarketDepthData(**data)
            self.data = depth
        else:
            raise TypeError(
                f"Unexpected empty data received when parsing message to MarketDept object. message: {kwargs}"
            )

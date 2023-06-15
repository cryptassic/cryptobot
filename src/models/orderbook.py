from enum import Enum
from typing import List
from dataclasses import dataclass


class EntryType(Enum):
    BID = "bid"
    ASK = "ask"


@dataclass
class MarketDepthEntry:
    type: EntryType
    price: str
    size: str


@dataclass
class MarketDepth:
    s: str  # Symbol name
    b: List[List[MarketDepthEntry]]  # Bids. Sorted by price in descending order
    a: List[List[MarketDepthEntry]]  # Asks. Sorted by price in asceding order
    u: int  # Update ID
    seq: int  # Cross Sequence Number


@dataclass
class OrderBook:
    topic: str  # Topic name
    type: str  # Snapshot or Delta
    ts: int  # The timestamp (ms) that the system generates the data
    data: MarketDepth

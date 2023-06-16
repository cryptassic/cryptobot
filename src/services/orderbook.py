from typing import Dict

from .buffer import Buffer

from models.marketdepth import MarketDepth


class OrderBook:
    ts: int
    symbol: str
    buffer: Buffer

    def __init__(
        self,
        symbol: str,
    ):
        self.symbol = symbol
        self.buffer = Buffer()

    def update(self, message):
        self.buffer.add(message)

    def get(self) -> MarketDepth:
        items = self.buffer.read()

        if items is not None and len(items) > 0:
            # return self.__select_buffer_candidate(items)
            return MarketDepth(**items[-1])

        return None

    def __select_buffer_candidate(self, items) -> MarketDepth:
        if not items:
            return None

        # We assume for simplicity, that message is of type MarketDepth
        min_item = min(items, key=lambda x: x["data"]["u"])
        max_item = max(items, key=lambda x: x["data"]["u"])

        # According to bybit docs, if u is 1 then we should use it as latest marketdepth snapshot
        # https://bybit-exchange.github.io/docs/v5/websocket/public/orderbook
        if min_item["data"]["u"] == 1:
            return MarketDepth(**min_item)
        else:
            return MarketDepth(**max_item)


class BookKeeper:
    books: Dict[str, OrderBook] = None

    @classmethod
    def get_instance(cls, symbol: str) -> OrderBook:
        # Ensure `books` is initialized
        if cls.books is None:
            cls.books = {}

        # Normalize the symbol
        symbol = symbol.lower()

        # If the order book for the symbol doesn't exist, create it
        if symbol not in cls.books:
            cls.books[symbol] = OrderBook(symbol)

        # Return the order book for the symbol
        return cls.books[symbol]

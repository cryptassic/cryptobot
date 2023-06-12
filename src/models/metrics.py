from dataclasses import dataclass


@dataclass
class Metrics:
    instance = None
    _tx_ts: int  # When data was sent
    _rx_ts: int  # When data was received
    _latency: int  # in milliseconds
    _trades_count: int
    _volatility: float
    _latest_price: float

    def __init__(
        self,
    ):
        self._tx_ts = 0
        self._rx_ts = 0
        self._latency = 0
        self._trades_count = 0
        self._volatility = 0
        self._latest_price = 0

    @property
    def tx_ts(self) -> int:
        return self._tx_ts

    @tx_ts.setter
    def tx_ts(self, value: int):
        self._tx_ts = value

    @property
    def rx_ts(self) -> int:
        return self._rx_ts

    @rx_ts.setter
    def rx_ts(self, value: int):
        self._rx_ts = value

    @property
    def latency(self) -> int:
        return self._latency

    @latency.setter
    def latency(self, value: int):
        self._latency = value

    @property
    def trades_count(self) -> int:
        return self._trades_count

    @trades_count.setter
    def trades_count(self, value: int):
        self._trades_count = value

    @property
    def volatility(self) -> float:
        return self._volatility

    @volatility.setter
    def volatility(self, value: float):
        self._volatility = value

    @property
    def latest_price(self) -> float:
        return self._latest_price

    @latest_price.setter
    def latest_price(self, value: float):
        self._latest_price = value

    @classmethod
    def get_instance(cls):
        if cls.instance is None:
            cls.instance = Metrics()
        return cls.instance

    def clear(self):
        self._latency = 0
        self._trades_count = 0
        self._volatility = 0
        self._latest_price = 0

    def __repr__(self) -> str:
        return f"ts: {{tx:{self.tx_ts}, rx:{self.rx_ts}, latency:{self.latency} ms}} trade_count: {self.trades_count} volatility: {format(self.volatility, '.8f')} latest_price: {self.latest_price}"

    def __str__(self) -> str:
        return f"ts: {{tx:{self.tx_ts}, rx:{self.rx_ts}, latency:{self.latency} ms}} trade_count: {self.trades_count} volatility: {format(self.volatility, '.8f')} latest_price: {self.latest_price}"

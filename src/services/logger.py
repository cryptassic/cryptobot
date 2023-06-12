import logging

LEVEL = logging.INFO


class Logger:
    logger: logging.Logger

    def __init__(self, name):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(LEVEL)

        self.logger.propagate = False

        c_handler = logging.StreamHandler()
        f_handler = logging.FileHandler(f"{name}.log")
        c_handler.setLevel(LEVEL)
        f_handler.setLevel(LEVEL)

        formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
        c_handler.setFormatter(formatter)
        f_handler.setFormatter(formatter)

        if not self.logger.handlers:
            self.logger.addHandler(c_handler)
            self.logger.addHandler(f_handler)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def debug(self, message):
        self.logger.debug(message)

    def log_trade(
        self,
        dispatch_ts: int,
        side: str,
        symbol: str,
        qty: str,
        price: str,
        type: str = "SINGLE",
    ):
        self.info(
            f"ts: {dispatch_ts} s: {symbol} S: {side} v: {qty} p: {price} t: {type}"
        )

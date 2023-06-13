import os
import logging
from pathlib import Path

LEVEL = logging.INFO

# LOGS_PATH = Logger.root_path()+"./logs"


def root_path() -> Path:
    from os.path import join, realpath

    return Path(realpath(join(__file__, "../../../")))


def create_folder():
    try:
        if not os.path.exists(Logger.LOGS_PATH):
            # Create the folder
            os.makedirs(Logger.LOGS_PATH)
    except Exception as e:
        print(e)


class Logger:
    logger: logging.Logger
    LOGS_PATH = root_path().joinpath("./logs")

    def __init__(self, name):
        self.path = Logger.LOGS_PATH.as_posix() + f"/{name}.log"

        create_folder()

        self.logger = logging.getLogger(name)
        self.logger.setLevel(LEVEL)

        self.logger.propagate = False

        c_handler = logging.StreamHandler()
        f_handler = logging.FileHandler(self.path)
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
        self.debug(
            f"ts: {dispatch_ts} s: {symbol} S: {side} v: {qty} p: {price} t: {type}"
        )

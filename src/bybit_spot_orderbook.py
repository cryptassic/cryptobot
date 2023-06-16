import argparse
from time import sleep

from client import Bybit
from services.logger import Logger

from models.db import BYBIT_ORDERBOOK

logger = Logger.getLogger("application")


def main(args):
    try:
        client = Bybit(
            server=args.server,
            instrument_type="spot",
            index=args.index,
            entity_type=BYBIT_ORDERBOOK,
        )

        # Subscribe to orderbook messages
        client.subscribe_orderbook()

        while True:
            # Keep looping
            sleep(1)
    except Exception as e:
        # Catch all exceptions not handled anywhere else
        logger.error(e)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Bybit Spot Trade Stream")

    # Add arguments
    parser.add_argument("--index", type=int, help="Bot index", default=0)
    parser.add_argument("--server", type=str, help="Server name", default="default")
    args = parser.parse_args()

    main(args)

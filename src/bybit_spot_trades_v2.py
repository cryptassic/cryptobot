import argparse
from time import sleep

from client import Bybit
from services.logger import Logger, get_identifier

logger = Logger.getLogger("application")


def main(args):
    try:
        client = Bybit(server=args.server, instrument_type="spot", index=args.index)

        # Subscribe to orderbook messages
        client.subscribe_trades()

        while True:
            # Keep looping
            sleep(1)
    except Exception as e:
        # Catch all exceptions not handled anywhere else
        logger.error(
            get_identifier("bybit", "spot_trades") + e,
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Bybit Spot Trade Stream")

    # Add arguments
    parser.add_argument("--index", type=int, help="Bot index", default=0)
    parser.add_argument("--server", type=str, help="Server name", default="default")
    args = parser.parse_args()

    main(args)

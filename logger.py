import logging


LOG_FORMAT = "%(asctime)s  %(levelname)-8s %(message)s"
LOG_DATE_FORMAT = "%H:%M:%S"


def setup_logger(name: str) -> logging.Logger:
    logging.basicConfig(
        level=logging.INFO,
        format=LOG_FORMAT,
        datefmt=LOG_DATE_FORMAT,
    )
    return logging.getLogger(name)

import logging
import logging.config
import sys

STREAM_FORMAT = "%(levelname)-8s %(asctime)s %(name)s:%(lineno)s %(message)s"
STREAM_SHORT_FORMAT = "%(asctime)s - %(message)s"

GCLOUD_NAME = "ask_me_emails"
GCLOUD_FORMAT = "%(name)s:%(lineno)s %(message)s"


def setup_stream_logger():
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter(STREAM_FORMAT))
    logging.getLogger().addHandler(handler)


def setup_stream_clean_logger():
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter(STREAM_SHORT_FORMAT))
    logging.getLogger().addHandler(handler)


def initialize_logging():
    setup_stream_logger()
    logging.getLogger().setLevel("INFO")

# Standard library
import os

# Internal modules
from app.config import util


DEVELOPMENT_PROFILE = "DEVELOPMENT"
TEST_PROFILE = "TEST"
PRODUCTION_PROFILE = "PRODUCTION"

PACKAGE_NAME = "stream-listener"
USER_AGENT = "mimir stream listener"
RPC_TIMEOUT = 1
THREAD_POOL_SIZE = int(os.getenv("THREAD_POOL_SIZE", default="2"))

APP_PROFILE = os.getenv("APP_PROFILE", PRODUCTION_PROFILE)
HANDLE_SPAM = os.getenv("HANDLE_SPAM", "FALSE") == "TRUE"
SPAM_LABEL = "SPAM"


FORBIDDEN_DOMAINS = set(
    [
        "owler.us",
        "owler.com",
        "stocktwits.com",
        "investorshangout.com",
        "1broker.com",
        "twitter.com",
        "cityfalcon.com",
        "mixlr.com",
    ]
)

REQUEST_ID_HEADER = "X-Request-ID"

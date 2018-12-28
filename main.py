# Standard library
import logging
import sys
from threading import Thread

# Internal modules
from app import stream_listner
from app import mq_connector
from app.service import emit_heartbeats
from app.config import HealthCheckConfig


_log = logging.getLogger(__name__)


def start_heartbeat_thread() -> None:
    """Configures and startes background thead for emiting liveness signs."""
    config = HealthCheckConfig()
    thread = Thread(target=emit_heartbeats, args=(config, mq_connector))
    thread.setDaemon(True)
    thread.start()


def main() -> None:
    try:
        start_heartbeat_thread()
        stream_listner.start()
    except Exception as e:
        _log.info("Exiting: {}".format(str(e)))
        sys.exit(1)


if __name__ == "__main__":
    main()

from enum import Enum
import logging
import colorlog
from colorlog import ColoredFormatter
import os


class LogType(Enum):
    DEBUG = 1
    DEVELOPMENT = 2
    PRODUCTION = 3


def get_log_type() -> LogType:
    log_type_env: str = os.getenv("ETABETA_LOG_TYPE", "production").lower()
    log_type = LogType.PRODUCTION
    if log_type_env in ["debug"]:
        log_type = LogType.DEBUG
    elif log_type_env in ["development", "dev"]:
        log_type = LogType.DEVELOPMENT
    elif log_type_env in ["production", "prod"]:
        log_type = LogType.PRODUCTION
    else:
        logging.error(
            f"Invalid ETABETA_LOG_TYPE '{log_type_env}'. Defaulting to {log_type.name}."
        )
    return log_type


def set_all_handler(handler: logging.Handler) -> None:
    """Set the given handler as the only handler for all existing loggers."""
    for logger in [logging.getLogger(name) for name in logging.root.manager.loggerDict]:
        logger.handlers = []
        logger.propagate = True
    logging.root.handlers = [handler]


def configure_dev_logging() -> None:
    color_console_handler = colorlog.StreamHandler()
    color_formatter = ColoredFormatter(
        "%(log_color)s%(levelname)-8s%(reset)s%(asctime)s %(bg_blue)s[%(name)s]%(reset)s %(message)s",
        datefmt="%H:%M:%S",
        reset=True,
        log_colors={
            "DEBUG": "cyan",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "red,bg_white",
        },
        secondary_log_colors={},
        style="%",
    )
    color_console_handler.setFormatter(color_formatter)
    set_all_handler(color_console_handler)

    logging.basicConfig(level=logging.INFO)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("uvicorn").setLevel(logging.INFO)
    logging.getLogger("etabeta").setLevel(logging.DEBUG)


def configure_debug_logging() -> None:
    configure_dev_logging()
    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger("uvicorn.access").setLevel(logging.DEBUG)
    logging.getLogger("uvicorn").setLevel(logging.DEBUG)


def configure_production_logging() -> None:
    console_handler = logging.StreamHandler()
    formatter = logging.Formatter(
        fmt="%(levelname)-8s%(asctime)s [%(name)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    console_handler.setFormatter(formatter)
    set_all_handler(console_handler)

    logging.basicConfig(level=logging.INFO)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("etabeta").setLevel(logging.INFO)


def configure_logging() -> None:
    log_type = get_log_type()
    if log_type == LogType.DEBUG:
        configure_debug_logging
    elif log_type == LogType.DEVELOPMENT:
        configure_dev_logging()
    elif log_type == LogType.PRODUCTION:
        configure_production_logging()
    logging.getLogger(__name__).debug(f"Logging configured for: {log_type.name}")

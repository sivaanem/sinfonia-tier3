import logging

import src.domain.format as fmt


_DEFAULT_FORMAT = "%(asctime)s  %(levelname)s  %(message)s"
_DEFAULT_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def _color_by_log_level(s: str, level: int) -> str:
    match level:
        case logging.DEBUG:
            return fmt.str.cyan(s)
        case logging.INFO:
            return fmt.str.white(s)
        case logging.WARNING:
            return fmt.str.yellow(s)
        case logging.ERROR:
            return fmt.str.red(s)
        case logging.CRITICAL:
            return fmt.str.red(s)
        case _:
            return fmt.str.white(s)


class DefaultFormatter(logging.Formatter):
    """Custom formatter class for API logging."""
    def __init__(
            self, 
            fmt: str = _DEFAULT_FORMAT,
            datefmt: str = _DEFAULT_DATE_FORMAT,
    ):
        super().__init__(fmt=fmt, datefmt=datefmt)

    def format(self, record: logging.LogRecord):                
        return _color_by_log_level(super().format(record), record.levelno)

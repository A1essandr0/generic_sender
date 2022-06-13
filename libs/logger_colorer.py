import logging


class ColoredFormatter(logging.Formatter):
    dark_grey = "\033[30m"
    grey = "\x1b[38;20m"
    white_on_grey = "\033[40m"
    light_blue = "\033[36m"
    dark_blue = "\033[34m"

    green = "\x1b[32m"

    yellow = "\x1b[33;20m"

    pink = "\x1b[35m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    white_on_red = "\033[41m"
    bold = "\033[1m"

    reset = "\x1b[0m"

    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"

    FORMATS = {
        logging.DEBUG: light_blue + format + reset,
        logging.INFO: bold + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


colored_stream = logging.StreamHandler()
colored_stream.setFormatter(ColoredFormatter())
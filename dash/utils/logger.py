# -*- coding: utf-8 -*-

import logging
import sys

from termcolor import colored


class _MyFormatter(logging.Formatter):
    def format(self, record):
        date = colored("[%(asctime)s @%(filename)s:%(lineno)d]", "green")
        msg = "%(message)s"
        if record.levelno == logging.WARNING:
            fmt = date + " " + colored("WARNING", "yellow", attrs=["blink"]) + " " + msg
        elif record.levelno == logging.ERROR or record.levelno == logging.CRITICAL:
            fmt = (
                date
                + " "
                + colored("ERROR", "red", attrs=["blink", "underline"])
                + " "
                + msg
            )
        elif record.levelno == logging.DEBUG:
            fmt = date + " " + colored("DEBUG", "magenta", attrs=["blink"]) + " " + msg
        else:
            fmt = date + " " + msg
        if hasattr(self, "_style"):
            # Python3 compatibility
            self._style._fmt = fmt
        self._fmt = fmt
        return super(_MyFormatter, self).format(record)


def get_logger(logger_name="logger"):
    """"""
    logger = logging.getLogger(logger_name)
    logger.propagate = False
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(_MyFormatter(datefmt="%y%m%d %H:%M:%S"))
    logger.addHandler(handler)

    return logger

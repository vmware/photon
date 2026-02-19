#!/usr/bin/env python3

import os
import logging
import threading


class Logger(object):
    _configured = False
    _lock = threading.Lock()

    @staticmethod
    def string_to_loglevel(loglevel):
        return {
            "error": logging.ERROR,
            "warning": logging.WARNING,
            "info": logging.INFO,
            "debug": logging.DEBUG,
        }.get(loglevel, logging.INFO)

    @staticmethod
    def getLogger(mymodule="Main", logpath=None, loglevel="info"):
        with Logger._lock:
            if Logger._configured:
                return logging.getLogger(mymodule)

            logfile = f"{mymodule}.log"
            if logpath:
                os.makedirs(logpath, exist_ok=True)
                logfile = f"{logpath}/{logfile}"

            root = logging.getLogger()
            root.setLevel(Logger.string_to_loglevel(loglevel))

            # File handler (ONE)
            fh = logging.FileHandler(logfile)
            fh.setFormatter(
                logging.Formatter("%(asctime)s - %(name)s - %(message)s")
            )

            # Console handler (ONE)
            ch = logging.StreamHandler()
            ch.setFormatter(logging.Formatter("%(message)s"))

            root.addHandler(fh)
            root.addHandler(ch)

            Logger._configured = True

        return logging.getLogger(mymodule)


if __name__ == "__main__":
    # Logger.getLogger("my module")
    t1 = Logger.getLogger("my module")
    t1.info("test1")

    t2 = Logger.getLogger("my module")
    t2.info("test2")

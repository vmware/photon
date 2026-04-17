#!/usr/bin/env python3

import logging
import threading
import weakref
import time
import os

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"

_loggers_alive = {}
# _loggers_alive maps builtin logging.Logger to our Logger class.
# Our Logger class holds the reference to the corresponding loging.Logger and file handle
# Let l = logging.getLogger(module)
#  1. Logger is not yet created: `l` not in _loggers_alive
#  2. Logger is known, but dead or just created: `_loggers_alive[l]` maps to a dead weak ref
#  3. Logger is alive: `_loggers_alive[l]` maps to a live weak ref
# State transitions:
#  1 -> 2 (lock held)
#  2 -> 3 (lock held)
#  3 -> 2 (lockless)

_lock = threading.Lock()
_console = logging.StreamHandler()
_console.setFormatter(logging.Formatter(LOG_FORMAT))

def _finalize_logger(l, fh):
    fh.close()
    l.removeHandler(fh)

class Logger(object):

    @staticmethod
    def string_to_loglevel(loglevel):
        return {
            "error": logging.ERROR,
            "warning": logging.WARNING,
            "info": logging.INFO,
            "debug": logging.DEBUG,
        }.get(loglevel, logging.INFO)

    @staticmethod
    def getLogger(module="Main", logpath=None, loglevel="info"):
        l = logging.getLogger(module)
        with _lock:
            logger_ref = _loggers_alive.get(l)
            if logger_ref is None:
                # module is not known yet
                l.setLevel(Logger.string_to_loglevel(loglevel))
                l.addHandler(_console)
            else:
                logger = logger_ref()
                if logger is not None:
                    # We are racing with some other thread, and the logger is alive again
                    return logger
            # module logger is dead, dying, or just created
            while len(l.handlers) > 1:
                # Yield and wait for the finalizer to complete
                time.sleep(0)
            logfile = f'{module}.log'
            if logpath is not None:
                os.makedirs(logpath, exist_ok=True)
                logfile = f'{logpath}/{logfile}'
            fh = logging.FileHandler(logfile)
            fh.setFormatter(logging.Formatter(LOG_FORMAT))
            l.addHandler(fh)
            logger = Logger(l)
            weakref.finalize(logger, _finalize_logger, l, fh)
            _loggers_alive[l] = weakref.ref(logger)
            return logger

    def debug(self, *args, **kwargs):
        self.l.debug(*args, **kwargs)

    def info(self, *args, **kwargs):
        self.l.info(*args, **kwargs)

    def warning(self, *args, **kwargs):
        self.l.warning(*args, **kwargs)

    def error(self, *args, **kwargs):
        self.l.error(*args, **kwargs)

    def exception(self, *args, **kwargs):
        self.l.exception(*args, **kwargs)

    def __init__(self, l):
        self.l = l


def test1(i):
    logger = Logger.getLogger('mymodule', loglevel='debug')
    logger.debug(f'test1 {i}')
    logger.info(f'test1 {i}')

def test2(i):
    logger = Logger.getLogger('mymodule', loglevel='debug')
    logger.warning(f'test2 {i}')
    logger.error(f'test2 {i}')

def thread_func(t, n):
    i = 0
    while n:
        t(i)
        n = n - 1
        i = i + 1

if __name__ == "__main__":
    t1 = threading.Thread(target=thread_func, args=(test1, 10000))
    t2 = threading.Thread(target=thread_func, args=(test2, 10000))
    t1.start()
    t2.start()
    t1.join()
    t2.join()

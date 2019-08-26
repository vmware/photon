import os
import logging

class Logger(object):
    @staticmethod
    def string_to_loglevel(loglevel):
        logLevelMap = {
            "error": logging.ERROR,
            "warning": logging.WARNING,
            "info": logging.INFO,
            "debug": logging.DEBUG,
        }
        return logLevelMap.get(loglevel, logging.INFO)

    @staticmethod
    def get_logger(logpath=None, loglevel="debug", console=False):
        logger = logging.getLogger("installer")
        if not logger.handlers:
            # file handler
            logfile = "installer.log"
            if logpath is not None:
                if not os.path.isdir(logpath):
                    os.makedirs(logpath)
                logfile = logpath + "/" + logfile
            fhandler = logging.FileHandler(logfile)
            fhformatter = logging.Formatter('%(asctime)s - %(message)s')
            fhandler.setFormatter(fhformatter)
            #fhandler.setLevel(logging.DEBUG)
            logger.addHandler(fhandler)

            # console handler
            if console:
                ch = logging.StreamHandler()
                if loglevel=="debug":
                    chformatter = logging.Formatter('%(asctime)s - %(message)s')
                else:
                    chformatter = logging.Formatter('%(message)s')
                ch.setFormatter(chformatter)
                #ch.setLevel(Logger.string_to_loglevel(loglevel))
                logger.addHandler(ch)

            logger.setLevel(Logger.string_to_loglevel(loglevel))
            logger.debug("-" * 75)
            logger.debug("Starting Log")
            logger.debug("-" * 75)
        return logger


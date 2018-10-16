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
    def getLogger(mymodule, logpath=None, loglevel="info"):
        logfile = mymodule + ".log"
        if logpath is not None:
            if not os.path.isdir(logpath):
                os.makedirs(logpath)
            logfile = logpath + "/" + logfile
        logger = logging.getLogger(mymodule)
        if not logger.handlers:
            #creating file handler
            fhandler = logging.FileHandler(logfile)
            # create console handler
            ch = logging.StreamHandler()
            fhformatter = logging.Formatter('%(asctime)s - %(name)s - %(message)s')
            chformatter = logging.Formatter('%(message)s')
            # add formatter to handler
            fhandler.setFormatter(fhformatter)
            #fhandler.setLevel(logging.DEBUG)
            ch.setFormatter(chformatter)
            #ch.setLevel(Logger.string_to_loglevel(loglevel))
            logger.setLevel(Logger.string_to_loglevel(loglevel))
            logger.addHandler(ch)
            logger.addHandler(fhandler)
            logger.debug("-" * 75)
            logger.debug("Starting Log")
            logger.debug("-" * 75)
        return logger

if __name__ == "__main__":
    #Logger.getLogger("my module")
    t1 = Logger.getLogger("my module")
    t1.info("test1")
    t2 = Logger.getLogger("my module")
    t2.info("test2")
    t1.info("test3")

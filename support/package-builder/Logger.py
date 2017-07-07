import logging
import os

class Logger(object):
    @staticmethod
    def getLogger (mymodule, logpath=None, resetFile=False):
        logfile=mymodule+".log"
        if logpath is not None:
            if not os.path.isdir(logpath):
                os.makedirs(logpath)
            logfile=logpath+"/"+logfile
        if resetFile:
            open(logfile, 'w').close()
        logger=logging.getLogger(mymodule)
        if len(logger.handlers) == 0:
            #creating file handler
            fhandler=logging.FileHandler(logfile)
            # create console handler
            ch=logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            # add formatter to handler
            fhandler.setFormatter(formatter)
            ch.setFormatter(formatter)

            logger.addHandler(ch)
            logger.addHandler(fhandler)
            logger.setLevel(logging.DEBUG)
            logger.info("--------------------------------------------------------------------------")
            logger.info("Starting Log")
            logger.info("--------------------------------------------------------------------------")
        return logger

if __name__ == "__main__":
    #Logger.getLogger("my module")
    t1 =  Logger.getLogger("my module")
    t1.info("test1")
    t2  = Logger.getLogger("my module")
    t2.info("test2")
    t1.info("test3")

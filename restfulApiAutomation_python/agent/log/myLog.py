import logging


class MyLog(object):
    def __init__(self):
        self.logger = logging.getLogger()
        format = '%(asctime)s[%(levelname)s]: %(message)s'
        self.formatter = logging.Formatter(format)
        # if not len(self.logger.handlers):
        if not self.logger.hasHandlers():
            self.logger.setLevel(logging.INFO)
            streamhandler = logging.StreamHandler()
            streamhandler.setFormatter(self.formatter)
            self.logger.addHandler(streamhandler)

    def debug(self, msg):
        self.logger.debug(msg)

    def info(self, msg):
        self.logger.info(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def error(self, msg):
        self.logger.error(msg)

    def critical(self, msg):
        self.logger.critical(msg)

    def log(self, level, msg):
        self.logger.log(level, msg)

    def setLevel(self, level):
        self.logger.setLevel(level)

    def logToFile(self, logFile):
        filehandler = logging.FileHandler(logFile, 'a', 'utf-8')
        filehandler.setFormatter(self.formatter)
        self.logger.addHandler(filehandler)

    def removeAllLogHandler(self):
        while(self.logger.hasHandlers()):
            self.logger.removeHandler(self.logger.handlers[0])

    def disable(self):
        logging.disable(50)

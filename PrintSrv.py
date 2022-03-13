import os
from subprocess import call
import sys
import pathlib
import log4p
from Singleton import Singleton


class WorkerThread(metaclass=Singleton):
    def __init__(self, callback):
        self.callback = callback
        self.running = True
        logger = log4p.GetLogger(__name__)
        self.log = logger.logger

    def worker(self):
        while self.running:
            tiemPolling = config.loopPollingTime()

class PrintSrv:
    def __init__(self):
        self.loggerInit()
        logger = log4p.GetLogger(__name__,config='./log4p.json')
        self.log =logger.loggger

    def loggerInit(self):
        if( os.name == 'posix '):
            logpath='~/AJB/logs/PrintSrv'
        else:
            logpath='C:/AJB/logs/PrintSrv'
        pathlib.Path(logpath, parents=True, exist_ok=True)

srv = PrintSrv()

#def main():

#    pass

if __name__ == '__main__':
    print(sys.version)
    
import os
from subprocess import call
import sys
import pathlib
from grpc import Call
import log4p
from Singleton import Singleton
from ConfigHelper import ConfigHelper
import time
import threading 
from TicketDb import TicketDb 
from TicketProcessor import TicketProcessor

config = ConfigHelper()
class WorkerThread(metaclass=Singleton):
    def __init__(self, callback):
        self.callback = callback
        self.running = True
        logger = log4p.GetLogger(__name__)
        self.log = logger.logger

    def worker(self):
        while self.running:
            timePolling = config.getLoopPollingTime()
            self.log.debug("timePolling: {}".format(timePolling))
            self.callback()
            time.sleep(int(timePolling))

    def start(self):
        self.thread = threading.Thread(target=self.worker)
        self.thread.start()
        self.log.debug("WorkerThread Started...")

    def stop(self):
        self.running=False
        self.thread.join()
        self.log.debug("WorkerThread Stopped..")

def Callback():
    pass
class PrintSrv:
    stoped = False
    presenter = None

    def __init__(self):
        self.loggerInit()
        logger = log4p.GetLogger(__name__, config='./log4p.json')
        self.log = logger.logger
        self.ticketDb = TicketDb() 
        self.ticketDb.watchQueue(TicketProcessor.process)
       #TODO: Eliminar el Worker thread salvo que sea para releer la configuracion 
        self.worker = WorkerThread(Callback)
        self.worker.start()
        self.ready = False

    def loggerInit(self):
        if os.name == "posix":
            logpath="~/AJB/logs/PrintSrv"
        else:
            logpath="C:/AJB/logs/PrintSrv"
        logpathlib = pathlib.Path(logpath)
        logpathlib.mkdir( parents=True, exist_ok=True)

    def onDestroy(self):
        self.worker.stop()
        
srv = PrintSrv()

if __name__ == '__main__':
    print(sys.version)
    srv.log.info(config)
    while True:
        pass
    srv.onDestroy()
    srv.log.debug("Bye")
    
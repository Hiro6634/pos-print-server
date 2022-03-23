import os
#from subprocess import call
import sys
import pathlib
#from grpc import Call
import log4p
from Singleton import Singleton
from ConfigHelper import ConfigHelper
import time
import threading 
from TicketDb import TicketDb 
from TicketProcessor import TicketProcessor

config = ConfigHelper()

class PrintSrv:
    stoped = False
    presenter = None

    def __init__(self):
        self.loggerInit()
        logger = log4p.GetLogger(__name__, config='./log4p.json')
        self.log = logger.logger
        self.ticketDb = TicketDb() 
        self.ticketDb.watchQueue(TicketProcessor().process)

    def loggerInit(self):
        print("OS: {}", os.name)
        if os.name == "posix":
            logpath="~/AJB/logs/PrintSrv"
        else:
            logpath="C:/AJB/logs/PrintSrv"

        logpathlib = pathlib.Path(logpath)
        logpathlib.mkdir( parents=True, exist_ok=True)
        
srv = PrintSrv()

if __name__ == '__main__':
    print(sys.version)
    srv.log.info(config)
    while True:
        pass
    
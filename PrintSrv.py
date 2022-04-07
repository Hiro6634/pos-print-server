import os
#from subprocess import call
import sys
import pathlib
#from grpc import Call
import log4p
from Singleton import Singleton
from ConfigHelper import ConfigHelper
import time
import schedule
from datetime import datetime
from TicketDb import TicketDb 
from TicketProcessor import TicketProcessor

config = ConfigHelper()

class PrintSrv:
    stoped = False
    presenter = None

    def __init__(self):
        self.loggerInit()
        logger = log4p.GetLogger(__name__, config='./log4p.json')
        self.configJob=0
        self.setConfigCheck()
        print(config.getTicketHeader())
        self.log = logger.logger
        self.ticketDb = TicketDb() 
        self.ticketDb.watchQueue(TicketProcessor().process)
        self.ticketDb.watchConfig(self.updateConfig)
        config.watchParam(ConfigHelper.TERMINAL_ID, self.updateWatchQueue)
        config.watchParam(ConfigHelper.CONFIG_POOLING_TIME_SEC, self.setConfigCheck)

    def updateConfig(self, prnConfig):
        killself = False
        print("SIMULATED: " + ( "True" if prnConfig["simulated"] is True else "False" ))
        print("TICKET HEADER: "+ prnConfig["ticket_header"])
        if "reboot" in prnConfig.keys():
            reboot = prnConfig["reboot"]
        else:
            reboot = False

        print("REBOOT: " + ( "True" if reboot is True else "False" ))
        if (reboot):
            killself = True

        if config.getSimulatePrinter() and not prnConfig["simulated"]:
            print("Printer Initializing...")
            #TicketProcessor().InitPrinter()
            killself = True


        config.setSimulatePrinter(prnConfig["simulated"])
        config.setTicketHeader(prnConfig["ticket_header"])
        config.writeConfigToFile();

        #TODO: Hasta póder resolver el tema de dessubscribirse del snapshot
        if killself:
            self.ticketDb.onReboot()

    def setConfigCheck(self):
        if self.configJob != 0:
            schedule.cancel_job(self.configJob) 
        self.configJob = schedule.every(config.getConfigPoolingTimeSec()).seconds.do(self.UpdateConfig)

    def updateWatchQueue(self):
        self.ticketDb.watchQueue(TicketProcessor().process)

    def loggerInit(self):
        print("OS: {}", os.name)
        if os.name == "posix":
            logpath="~/AJB/logs/PrintSrv"
        else:
            logpath="C:/AJB/logs/PrintSrv"

        logpathlib = pathlib.Path(logpath)
        logpathlib.mkdir( parents=True, exist_ok=True)
        
    def UpdateConfig(self):
        config.readConfigFromFile()

srv = PrintSrv()

if __name__ == '__main__':
    print(sys.version)
    srv.log.info(config)
    while True:
        schedule.run_pending()
        time.sleep(1)
        pass
    
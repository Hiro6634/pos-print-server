import json
from os import path
from Singleton import Singleton
import log4p

class ConfigHelper(metaclass=Singleton):
    configFile = "Ajbpos.config"
    config_dict = json.loads("{}")
    TERMINAL_ID = 'terminalId'
    DATA_SERVER_ADDR = 'dataServerAddr'
    DATA_SERVER_PORT = 'dataServerPort'
    PRINT_SERVER_URL = 'printServerUrl'
    PRINT_SERVER_ADDR = 'printServerAddr'
    PRINT_SERVER_PORT = 'printServerPort'
    TICKET_HEADER = 'ticketHeader'
    PRODUCT_POLLING_TIME = 'productPollingTime'
    PRODUCT_STATE_POLLING_TIME_IN_SEC = 'productStatePollingTimeInSec'
    SIMULATE_PRINTER = 'simulatePrinter'
    PRINTER_NAME = 'PrinterName'
    LOOP_POLLING_TIME = 'LoopPollingTime'
    initialized = False    

    #########################################################
    ##  DEFAULT VALUES 
    #########################################################
    Def_TerminalId = '0001'
    Def_DataServerAddr = '127.0.0.1'
    Def_DataServerPort = 8000
    Def_PrintServerAddr = '127.0.0.1'
    Def_PrintServerPort = 9000
    Def_LocalPrint = False
    Def_TicketHeader = '9° BURZACO MATSURI'
    Def_ProductPollingTime = 30
    Def_ProductStatePollingTimeInSec = 10
    Def_SimulatePrinter = False
    Def_PrinterName = 'EPSON TM-T20II Receipt'
    Def_LoopPollingTime = 30
    #########################################################
    ##  Configuration Object
    #########################################################
    
    def __init__(self, configFile = ''):
        logger = log4p.GetLogger(__name__)
        self.log = logger.logger
        self.configFile = configFile if len(configFile) > 0 else self.configFile
        self.readConfigFromFile()
        self.initialized = False if self.TERMINAL_ID not in self.config_dict else True

    def updateParam( self, param, value):
        modified = False
        self.log.debug("{}:{}".format(param,value))
        if param in self.config_dict:
            # self.log.debug("Param: {} found!".format(param))
            pType=type(self.config_dict[param])
            modified = True
            if pType is str:
                modified = True
                self.config_dict[param] = str(value)
            elif pType is int:
                modified = True
                self.config_dict[param] = int(value)
            elif pType is float:
                modified = True
                self.config_dict[param] = float(value)
            else:
                self.log.error("Param: {} type unknown".format(param))
        if modified:
            self.writeConfigToFile()

    def readConfigFromFile(self):
        if path.exists(self.configFile):
            with open(self.configFile, encoding="utf-8") as json_file:
                self.config_dict = json.load(json_file)

    def writeConfigToFile(self):
        print("writeConfigToFile")
        with open(self.configFile, 'wt', encoding="utf-8") as outfile:
            json.dump(self.config_dict, outfile)

    def isInitialized(self):
        return self.initialized
        
    def setTerminalId(self, terminalId):
        self.config_dict[self.TERMINAL_ID]=terminalId
        self.initialized = True

    def getTerminalId(self):
        return self.config_dict[self.TERMINAL_ID] \
            if self.TERMINAL_ID in self.config_dict else self.Def_TerminalId

    def setDataServerAddr(self, value):
        self.config_dict[self.DATA_SERVER_ADDR]=value


    def getDataServerAddr(self):
        return self.config_dict[self.DATA_SERVER_ADDR] \
            if self.DATA_SERVER_ADDR in self.config_dict else self.Def_DataServerAddr

    def setDataServerPort(self, value):
        self.config_dict[self.DATA_SERVER_PORT]=value 
        
    def getDataServerPort(self):
        return self.config_dict[self.DATA_SERVER_PORT] \
            if self.DATA_SERVER_PORT in self.config_dict else self.Def_DataServerPort

    def setPrintServerAddr(self, value):
        self.config_dict[self.PRINT_SERVER_ADDR]=value

    def getPrintServerAddr(self):
        return self.config_dict[self.PRINT_SERVER_ADDR] \
            if self.PRINT_SERVER_ADDR in self.config_dict else self.Def_PrintServerAddr
    
    def setPrintServerPort(self,value):
        self.config_dict[self.PRINT_SERVER_PORT]=value

    def getPrintServerPort(self):
        return self.config_dict[self.PRINT_SERVER_PORT] \
            if self.PRINT_SERVER_PORT in self.config_dict else self.Def_PrintServerPort
    
    def getPrintServerUrl(self):
        return "{}:{}".format(self.getPrintServerAddr(), self.getPrintServerPort())

    def setTicketHeader(self, value):
        self.config_dict[self.TICKET_HEADER]=value
    
    def getTicketHeader(self):
        return self.config_dict[self.TICKET_HEADER] \
            if self.TICKET_HEADER in self.config_dict else self.Def_TicketHeader
    
    def setProductPollingTime(self, value):
        self.config_dict[self.PRODUCT_POLLING_TIME] = value

    def getProductPollingTime(self):
        return self.config_dict[self.PRODUCT_POLLING_TIME] \
            if self.PRODUCT_POLLING_TIME in self.config_dict else self.Def_ProductPollingTime    
    
    def setProductStatePollingTimeInSec(self, value):
        self.config_dict[self.PRODUCT_STATE_POLLING_TIME_IN_SEC] = value

    def getProductStatePollingTimeInSec(self):
        return self.config_dict[self.PRODUCT_STATE_POLLING_TIME_IN_SEC] \
            if self.PRODUCT_STATE_POLLING_TIME_IN_SEC in self.config_dict else self.Def_ProductStatePollingTimeInSec
    
    def setSimulatePrinter(self, value):
        self.config_dict[self.SIMULATE_PRINTER] = value

    def getSimulatePrinter(self):
        return self.config_dict[self.SIMULATE_PRINTER] \
            if self.SIMULATE_PRINTER in self.config_dict else self.Def_SimulatePrinter

    def getPrinterName(self):
        return self.config_dict[self.PRINTER_NAME] \
            if self.PRINTER_NAME in self.config_dict else self.Def_PrinterName

    def getLoopPollingTime(self):
        # self.log.debug(json.dumps(self.config_dict, indent = 2))
        res = self.config_dict[self.LOOP_POLLING_TIME] \
            if self.LOOP_POLLING_TIME in self.config_dict else self.Def_ProductPollingTime    
        # self.log.debug("PPT:{}".format(res))
        return res

    def setLoopPollingTime(self, value):
        self.config_dict[self.LOOP_POLLING_TIME] = value

    def __str__(self):
        return """
    PrintServerAddr: {}
    PrintServerPort: {}
    PrintServerUrl: {}
    SimulatePrinter: {}
    PrinterName: {}
        """.format(
            self.getPrintServerAddr(),
            self.getPrintServerPort(),
            self.getPrintServerUrl(),
            self.getSimulatePrinter(),
            self.getPrinterName())
            

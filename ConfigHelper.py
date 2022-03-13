import json
from os import path
from Singleton import Singleton
import log4p 

class ConfigHelper(metaclass=Singleton):
    configFile = "Ajbpos.config"
    config_dict = json.loads("{}")
    TERMINAL_ID = 'TerminalId'
    DATA_SERVER_ADDR = 'DataServerAddr'
    DATA_SERVER_PORT = 'DataServerPort'
    PRINT_SERVER_URL = 'PrintServerUrl'
    PRINT_SERVER_ADDR = 'PrintServerAddr'
    PRINT_SERVER_PORT = 'PrintServerPort'
    TICKET_HEADER = 'TicketHeader'
    LOOP_POLLING_TIME = 'LoopPollingTime'
    PRODUCT_POLLING_TIME = 'ProductPollingTime'
    PRODUCT_STATE_POLLING_TIME_IN_SEC = 'ProductStatePollingTimeInSec'
    SHEET_RECONNECTIONS_TRIES = 'SheetReconnectionTries'
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
    Def_LoopPollingTime = 30
    Def_ProductPollingTime = 30
    Def_ProductStatePollingTimeInSec = 10
    Def_SheetReconnectionTries = 3

    #########################################################

    def __init__(self):
        logger = log4p.GetLogger(__name__)
        self.log = logger.logger 
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
        with open(self.configFile, 'w', encoding="utf-8") as outfile:
            json.dump(self.config_dict, outfile)

    def isInitialized(self):
        return self.initialized
        
    def setLoopPollingTime(self, loopPollingTime):
        self.config_dict[self.LOOP_POLLING_TIME] = loopPollingTime

    def getLoopPollingTime(self):
        return self.config_dict[self.LOOP_POLLING_TIME] \
            if self.LOOP_POLLING_TIME in self.config_dict else self.Def_LoopPollingTime 

    def setTerminalId(self, terminalId):
        self.config_dict[self.TERMINAL_ID]=terminalId

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
        # self.log.debug(json.dumps(self.config_dict, indent = 2))
        res = self.config_dict[self.PRODUCT_POLLING_TIME] \
            if self.PRODUCT_POLLING_TIME in self.config_dict else self.Def_ProductPollingTime    
        # self.log.debug("PPT:{}".format(res))
        return res

    def setProductStatePollingTimeInSec(self, value):
        self.config_dict[self.PRODUCT_STATE_POLLING_TIME_IN_SEC] = value
 
    def getSheetReconnectionTries(self):
        return self.config_dict[self.SHEET_RECONNECTIONS_TRIES] \
            if self.SHEET_RECONNECTIONS_TRIES in self.config_dict else self.Def_SheetReconnectionTries

    def setSheetReconnectionTries(self, value):
        self.config_dict[self.SHEET_RECONNECTIONS_TRIES] = value

    def __str__(self):
        return """
    DataServerAddr: {}
    DataServerPort: {}
    ProductPollingTime: {}
        """.format(
            self.getDataServerAddr(),
            self.getDataServerPort(),
            self.getProductPollingTime())
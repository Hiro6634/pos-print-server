import json
from os import path
from Singleton import Singleton
import log4p
import pathlib

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
    PRINTER_VENDORID = 'PrinterVendorId'
    PRINTER_PRODUCTID = 'PrinterProductId'
    PRN_DPI = 'prn_dpi'
    PRN_INCHES_WIDTH = 'prnInchesWidth'
    CONFIG_POOLING_TIME_SEC = 'configPoolingTimeSec'
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
    Def_TicketHeader = '10° BURZACO MATSURI'
    Def_ProductPollingTime = 30
    Def_ProductStatePollingTimeInSec = 10
    Def_SimulatePrinter = False
    Def_ConfigPoolingTimeSec = 60
    
    Def_PrinterName = 'EPSON TM-T20II Receipt'
    Def_LoopPollingTime = 30
    Def_PrinterVendorId = 0x04b8
    Def_PrinterProductId = 0x0e15
    Def_prn_dpi = 203
    Def_prn_inches_width = 2.83465

    #########################################################
    ##  Configuration Object
    #########################################################
    
    def __init__(self, configFile = ''):
        self.watchlist = {}
        logger = log4p.GetLogger(__name__)
        self.log = logger.logger
        self.configFile = configFile if len(configFile) > 0 else self.configFile
        self.lastModificationTime = 0
        self.readConfigFromFile()
        self.initialized = False if self.TERMINAL_ID not in self.config_dict else True
        
    def job(self):
        print("BINGO DOBLE!")

    def watchParam(self, param, watcher):
        self.watchlist[param] = watcher

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
        lstModTime = pathlib.Path(self.configFile).stat().st_mtime
        if lstModTime != self.lastModificationTime:
            self.lastModificationTime = lstModTime
            if path.exists(self.configFile):
                with open(self.configFile, encoding="utf-8") as json_file:
                    self.config_dict = json.load(json_file)
                for param in self.config_dict:
                    if param in self.watchlist:
                        self.watchlist[param]()
            print("Configuration File updated")
        else:
            print("Configuration File was not modified")

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

    def setPrinterVendorId(self, value):
        self.config_dict[self.PRINTER_VENDORID] = value
    
    def getPrinterVendorId(self):
        return self.config_dict[self.PRINTER_VENDORID] \
            if self.PRINTER_VENDORID in self.config_dict else self.Def_PrinterVendorId

    def setPrinterProductId(self, value):
        self.config_dict[self.PRINTER_PRODUCTID] = value
    
    def getPrinterProductId(self):
        return self.config_dict[self.PRINTER_PRODUCTID] \
            if self.PRINTER_PRODUCTID in self.config_dict else self.Def_PrinterProductId

    def setPrnDpi(self, value):
        self.config_dict[self.PRN_DPI] = value
    
    def getPrnDpi(self):
        return self.config_dict[self.PRN_DPI] \
            if self.PRN_DPI in self.config_dict else self.Def_prn_dpi

    def setPrnInchesWidth(self, value):
        self.config_dict[self.PRN_INCHES_WIDTH] = value
    
    def getPrnInchesWidth(self):
        return self.config_dict[self.PRN_INCHES_WIDTH] \
            if self.PRN_INCHES_WIDTH in self.config_dict else self.Def_prn_inches_width

    def setConfigPoolingTimeSec(self, value):
        self.config_dict[self.CONFIG_POOLING_TIME_SEC] = value
    
    def getConfigPoolingTimeSec(self):
        return self.config_dict[self.CONFIG_POOLING_TIME_SEC] \
            if self.CONFIG_POOLING_TIME_SEC in self.config_dict else self.Def_ConfigPoolingTimeSec

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
            
if __name__=="__main__":
    config = ConfigHelper()

    while True:
        pass
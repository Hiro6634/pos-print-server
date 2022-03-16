import log4p
from Ticket import Ticket
from PrintRepository import PrintRepository
from PrintRepository import FontBuilder
from ConfigHelper import ConfigHelper
import json

config = ConfigHelper()

class TicketProcessor:

    def __init__(self):
        logger = log4p.GetLogger(__name__, config='./log4p.json')
        self.log = logger.logger
        self.printRepo = PrintRepository()

    def process(self, ticket ):
        ticketObj = Ticket( ticket)
        self.printRepo.PrintDoc( \
            config.getPrinterName(), \
            config.getTicketHeader(), \
            self.buildInvoice(ticketObj))        

        for item in ticketObj.getItems():
            for q in range(0,item.getQuantity()):
                self.printRepo.PrintDoc( \
                    config.getPrinterName(), \
                    config.getTicketHeader(), \
                    self.buildVoucher(item))
    
        
    ################################################
    ## Invocie Formating
    ################################################
    def buildInvoice(self, ticket):
        println = []
        
        println.append(self.printRepo.PrintLine(config.getTicketHeader(), FontBuilder.H4, "center"))
        println.append(self.printRepo.PrintLine("", FontBuilder.H2Bold, "center"))
        for item in ticket.getItems():
            line = "{} x {} ${}".format(item.getQuantity(), item.getDescription(), item.getSubtotal())
            println.append(self.printRepo.PrintLine(line, FontBuilder.H3,"left"))
        line = "TOTAL ${}".format(ticket.getTotal())

        println.append(self.printRepo.PrintLine(line, FontBuilder.H4,"right"))
        println.append(self.printRepo.PrintLine("", FontBuilder.H4,"right"))
        println.append(self.printRepo.PrintLine("VENDEDOR:"+ticket.getDisplayName(), FontBuilder.H3,"right"))
        println.append(self.printRepo.PrintLine(ticket.getPrintAt(), FontBuilder.H3,"right"))
        return println

    ################################################
    ## Voucher Formating
    ################################################
    def buildVoucher(self, item):
        println = []
        
        println.append(self.printRepo.PrintLine(config.getTicketHeader(), FontBuilder.H3, "center"))
        println.append(self.printRepo.PrintLine("", FontBuilder.H3, "center"))
        println.append(self.printRepo.PrintLine(item.getDescription(), FontBuilder.H1Bold,"center"))

        return println

if __name__ == '__main__':
    mockTicket = json.loads('{"total": 510, "printAt": "2022-03-15T22:44:59.770Z", "items": [{"subtotal": 360, "price": 180, "quantity": 2, "category": "PARRILLA", "description": "BONDIOLA"}, {"category": "parrilla", "price": 150, "quantity": 1, "description": "CHORIPAN", "subtotal": 150}], "user": {"displayName": "Hiro Suyama", "email": "hiro.suyama+matsuri@gmail.com"}}')
    tkm = TicketProcessor()
    tkm.log.info(config)
    tkm.process(mockTicket)

    pass
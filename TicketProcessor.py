import cmd
import log4p
from Ticket import Ticket
from PrintRepository import PrintRepository
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
                    self.buildVoucher(item, str(ticketObj.getPrintAt())))

    ################################################
    ## Invoice Formating
    ################################################
    def buildInvoice(self, ticket):
        println = []
        headerFont = PrintRepository.VARELA_ROUND
        lineFont = PrintRepository.VARELA_ROUND
        totalFont = PrintRepository.VARELA_ROUND
        footerFont = PrintRepository.VARELA_ROUND

        #TODO: Hay qie poner los fonts en una coleccion
        println.append(
            self.printRepo.PrintLine(
                config.getTicketHeader(), 
                font = headerFont,
                size=40,
                align=PrintRepository.CENTER
            )
        )
        println.append(
            self.printRepo.PrintLine(
                "=============================================", 
                font = lineFont,
                size=25,
                align=PrintRepository.RIGHT
            )
        )
        for item in ticket.getItems():
            line = "{} x {} ${}".format(item.getQuantity(), item.getDescription(), item.getSubtotal())
            println.append(
                self.printRepo.PrintLine(
                    line, 
                font = lineFont,
                size=25,
                align=PrintRepository.RIGHT
                )
            )
        println.append(
            self.printRepo.PrintLine(
                "=============================================", 
                font = lineFont,
                size=25,
                align=PrintRepository.RIGHT
            )
        )

        line = "TOTAL ${}".format(ticket.getTotal())

        println.append(
            self.printRepo.PrintLine(
                line, 
                font = totalFont,
                size=50,
                align=PrintRepository.RIGHT
            )
        )
        println.append(self.printRepo.PrintLine(cmd=PrintRepository.LF))
        println.append(
            self.printRepo.PrintLine(
                "VENDEDOR:"+ticket.getDisplayName() + "          " + str(ticket.getPrintAt()), 
                font = footerFont,
                size=20,
                align=PrintRepository.CENTER
            )
        )
        println.append(self.printRepo.PrintLine(cmd=PrintRepository.CUT))
        return println

    ################################################
    ## Voucher Formating
    ################################################
    def buildVoucher(self, item, printAt):
        headerFont = PrintRepository.VARELA_ROUND
        lineFont = PrintRepository.MPLUS_ROUNDED_EB
        footerFont = PrintRepository.VARELA_ROUND
        println = []
        
        println.append(
            self.printRepo.PrintLine(
                config.getTicketHeader(),                                                                                                                       
                font = headerFont,
                size=40,
                align=PrintRepository.CENTER
            )
        )
        println.append(self.printRepo.PrintLine(cmd=PrintRepository.LF))
        println.append(
            self.printRepo.PrintLine(
                item.getDescription(), 
                font = lineFont,
                size=150,
                align=PrintRepository.CENTER
            )
        )
        println.append(self.printRepo.PrintLine(cmd=PrintRepository.LF))
        println.append(
            self.printRepo.PrintLine(
                printAt, 
                font = footerFont,
                size=20,
                align=PrintRepository.RIGHT
            )
        )
        println.append(self.printRepo.PrintLine(cmd=PrintRepository.CUT))

        return println

if __name__ == '__main__':
    mockTicket = json.loads('{"total": 510, "printAt": "2022-03-15T22:44:59.770Z", "items": [{"subtotal": 360, "price": 180, "quantity": 2, "category": "PARRILLA", "description": "BONDIOLA"}, {"category": "parrilla", "price": 150, "quantity": 1, "description": "CHORIPAN", "subtotal": 150}], "user": {"displayName": "Hiro Suyama", "email": "hiro.suyama+matsuri@gmail.com"}}')
    tkm = TicketProcessor()
    tkm.log.info(config)
    tkm.process(mockTicket)

    pass
from Ticket import Ticket

class TicketProcessor:
    def process(self, ticket ):
        self.ticket = Ticket( ticket)
        print(ticket)        
        print("=============================")
        for item in self.ticket.getItems():
            for q in range(0,item.getQuantity()):
                print(item.getDescription())
        print("-----------------------------")
        pass
    
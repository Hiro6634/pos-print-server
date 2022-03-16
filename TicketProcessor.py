from Ticket import Ticket

class TicketProcessor:
    def process(self, ticket ):
        self.ticket = Ticket( ticket)

        print(self.ticket.getDisplayName()) 
        print(str(self.ticket))           
        pass
    
class Ticket:
    def __init__(self):
        pass

    def Process(self, ticket):
        if 'user' in ticket:
            print(ticket['user']['displayName'])
        if 'items' in ticket:
            for item in ticket['items']:
                print(str(item['quantity'])+ "  "+ item['description'])
            

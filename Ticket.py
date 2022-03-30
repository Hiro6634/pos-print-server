from Item import Item

class Ticket:
    USER = "user"
    ITEMS = "items"
    DISPLAY_NAME = "displayName"
    EMAIL = "email"
    TOTAL = "total"
    PRINT_AT = "printAt"
    TOTAL = "total"
    TEST = "test"
    def __init__(self,ticket):
        if self.USER in ticket:
            user = ticket[self.USER]
            self.displayName= user[self.DISPLAY_NAME]  if (self.DISPLAY_NAME in user) else ""
            self.email=user[self.EMAIL] if self.EMAIL in user else ""
        self.printAt=ticket[self.PRINT_AT] if self.PRINT_AT in ticket else ""
        self.total=ticket[self.TOTAL] if self.TOTAL in ticket else 0

        self.items = []
        if self.ITEMS in ticket:
            for item in ticket[self.ITEMS]:
                __item = Item(item)
                self.items.append(__item)
        self.test = ticket[self.TEST] if self.TEST in ticket else False

    def getDisplayName(self):
        return self.displayName

    def getEmail(self):
        return self.email

    def getPrintAt(self):
        return self.printAt

    def getTotal(self):
        return self.total

    def getItems(self):
        return self.items

    def isTest(self):
        return self.test == True

    def __str__(self):
        return 'Ticket [displayName=' + self.displayName + ', email=' + self.email + ', printAt=' + str(self.printAt) + ', total=' + str(self.total) + 'items=' + str(self.items) + ']' 

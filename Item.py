class Item:
    CATEGORY = "category"
    DESCRIPTION = "description"
    QUANTITY = "quantity"
    PRICE = "price"
    SUBTOTAL = "subtotal"

    def __init__(self, item):
        self.category = item[self.CATEGORY] if self.CATEGORY in item else ""
        self.description = item[self.DESCRIPTION] if self.DESCRIPTION in item else ""
        self.quantity = item[self.QUANTITY] if self.QUANTITY in item else 0
        self.price = item[self.PRICE] if self.PRICE in item else 0
        self.subtotal = item[self.SUBTOTAL] if self.SUBTOTAL in item else 0

    def getCategory(self):
        return self.category

    def getDescription(self):
        return self.description
    
    def getQuantity(self):
        return self.quantity

    def getPrice(self):
        return self.price

    def getSubtotal(self):
        return self.subtotal

    def __str__(self):
        return 'Item [category:' + self.category + ', description:' + self.description + ', quantity:' + str(self.quantity) + ', price:' + str(self.price) + ', subtotal:' + str(self.subtotal) + ']'
        
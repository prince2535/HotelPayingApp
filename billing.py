#create a class to store detail of one order
class Order:
    #constructore use when order create
    def __init__(self,item_name,quantity,price_per_item):
        self.item_name = item_name #e.g,tea
        self.quantity = quantity  #e.g,2
        self.price_per_item = price_per_item #e.g,10 (₹)
      
     
     #method to calculate total price = quantity*price
    def total_price(self):
        return self.quantity*self.price_per_item    
        
        
    
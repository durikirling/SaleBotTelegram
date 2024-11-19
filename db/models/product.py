from .generic import GenericItem
from time import time

class Product(GenericItem): 

    table_name = 'products'
    create_sql = '''
        id INT NOT NULL PRIMARY KEY,
        size FLOAT NOT NULL,
        new_price FLOAT NOT NULL,
        old_price FLOAT NOT NULL,
        url TEXT NOT NULL,
        in_stock BOOL NOT NULL,
        last_update FLOAT        
    '''

    def __init__(self, 
        sku, 
        size=0, 
        new_price=0, 
        old_price=0, 
        url="https://", 
        in_stock=False,
        last_update=time()
    ):
        self.id = sku
        self.size = size
        self.new_price = new_price
        self.old_price = old_price
        self.url = url
        self.in_stock = in_stock
        self.last_update = last_update

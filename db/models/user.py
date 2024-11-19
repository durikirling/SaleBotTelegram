from .generic import GenericItem

class User(GenericItem): 

    table_name = 'users'
    create_sql = '''
        ID INT NOT NULL PRIMARY KEY,
        chat_id INT NOT NULL,
        activated BOOL NOT NULL,
        discount INT        
    '''

    def __init__(self, 
        id, 
        chat_id=None, 
        activated=False, 
        discount=0
    ):
        self.id = id
        self.chat_id = chat_id if chat_id else id
        self.activated = activated
        self.discount = discount

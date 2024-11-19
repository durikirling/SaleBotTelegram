# import os, sys
# sys.path.append('..')
from ..database import db

class GenericItem:

    def __get_selection__(self):
        data = db.select_item(self.table_name, None, f'id={self.id}')
        if len(data) == 0:
            return None
        return data[0]
    
    def __get_instance_attributes__(self):
        result = list()
        for attribute, value in self.__dict__.items():
            result.append(attribute)
        return result

    def save(self): # or upload_data or upload_to_db
        db_user = self.__get_selection__()
        if db_user is not None:
            print('edit item')
            db.edit_item(self.table_name, self.id, self)
        else:
            print('create item')
            db.add_item(self.table_name, self)

    def delete(self):
        db_user = self.__get_selection__()
        if db_user is not None:
            print('delete item')
            db.delete_item(self.table_name, self.id)
        else:
            print("item not found")
    
    def sync_data(self): # or load_data or load_to_db
        data = self.__get_selection__()
        if data is not None:
            for item in data:
               setattr(self, item, data[item])
            print('data loaded from db')
            return True
        else:
            return False
        
    def get_all(self):
        return db.select_item(self.table_name)

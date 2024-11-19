from .database import db
from .models import *

def run():
    tables = [
        # User(0),
        Product(0)
    ]

    for item in tables:
        # attrs = item.__get_instance_attributes__()
        # print(attrs)
        # attrs_str = ', '.join(attrs)
        # print(attrs_str)
        db.create_table(item.table_name, item.create_sql)
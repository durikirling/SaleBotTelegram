import os, sqlite3
from typing import Union

class Database:
    def __init__(self, db_name: str):
        '''Конструктор класса. Определяет файл базы данных'''
        self.__db_path = os.getcwd()
        # self.db_name = os.path.join(self.__db_path, db_name)
        self.db_name = os.path.join(self.__db_path + '\db', db_name)

    def __connect(self):
        '''Функция подключения к базе данных'''
        connect = sqlite3.connect(self.db_name)
        return connect
    
    def create_table(self, table_name: str, fields: str):
        '''Создание таблицы в БД'''
        with self.__connect() as connect:
            cursor = connect.cursor()
            drop_row_sql = f"""DROP TABLE IF EXISTS {table_name};"""
            cursor.execute(drop_row_sql)
            create_row_sql = f"""CREATE TABLE {table_name} ({fields});"""
            cursor.execute(create_row_sql)
            print("Table is Ready")
    
    def get_column_names(self, table_name: str) -> list[str]: 
        '''Получение наименований колонок таблицы'''
        with self.__connect() as connect:
            cursor = connect.cursor()
            pragma_row_sql = f"""PRAGMA table_info({table_name});"""
            selector = cursor.execute(pragma_row_sql)
            column_names = [i[1] for i in selector.fetchall()]
            return column_names
    
    def select_item(self, 
            table_name: str, 
            column_names:Union[None,str,list[str]] = None, 
            filter:Union[str,None]=None
    ) -> list[dict]:
        '''Получение данных из БД'''
        with self.__connect() as connect:
            cursor = connect.cursor()

            if column_names is None or column_names == "*" or len(column_names) == 0:
                column_names = self.get_column_names(table_name)
                fields_string = '*'
            else:
                fields_string = ', '.join(column_names)

            select_row_sql = f"""SELECT {fields_string} FROM {table_name}"""
            if filter:
                select_row_sql += f""" WHERE {filter}"""
            select_row_sql += ';'

            selector = cursor.execute(select_row_sql)
            resultList = list()
            for item in selector.fetchall():
                resultItem = dict()
                for i in range(len(column_names)):
                    resultItem[column_names[i]] = item[i]
                resultList.append(resultItem)
            return resultList
        
    def add_item(self, table_name:str, data):
        '''Создание записи в БД'''
        with self.__connect() as connect:
            cursor = connect.cursor()
            column_names = self.get_column_names(table_name)
            data_string = ('?, ' * len(column_names))[0:-2]
            data_tuple = tuple()
            for item in column_names:
                value = getattr(data, item)
                data_tuple += (value,)
            # attrs = data.__get_instance_attributes__()
            # attrs_str = ', '.join(attrs)
            # ({attrs_str}) 
            insert_row_sql = f"""
                INSERT INTO {table_name}
                VALUES({data_string});
            """
            cursor.execute(insert_row_sql, data_tuple)

    def delete_item(self, table_name:str, id:int):
        '''Удаление записи из БД'''
        with self.__connect() as connect:
            cursor = connect.cursor()
            delete_row_sql = f"""DELETE FROM {table_name} WHERE id={id};"""
            cursor.execute(delete_row_sql)

    def edit_item(self, table_name:str, id:int, edit_data):
        '''Редактирование записи в БД'''
        with self.__connect() as connect:
            edit_str = ''
            data_tuple = tuple()
            for item in edit_data.__get_instance_attributes__():
                edit_str += f'{item} = ?, '
                data_tuple += (getattr(edit_data, item),)
            edit_str = edit_str[0:-2]
            cursor = connect.cursor()
            update_row_sql = f"""
                UPDATE {table_name} 
                SET {edit_str} 
                WHERE id={id};
            """
            cursor.execute(update_row_sql, data_tuple)

db_name = 'database.db'
db = Database(db_name)

# insert_stmt = (
#     "INSERT INTO users (ID, Chat_id, Activated, Discount) "
#     "VALUES (?, ?, ?, ?)"
# )
# data1 = (286499341, 286499341, True, 20)
# data2 = (696399662, 696399662, True, 20)
# db.add_item(insert_stmt, data2)
# db.add_item('users', {'id': 1, 'chat_id': 2, 'activated': False, 'discount': 0})

# print(db.select_item('users', ['id', 'discount']))

# db.create_table('users', 'id, chat_id, activated, discount')
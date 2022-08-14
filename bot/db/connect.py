import os
import sqlite3 as db

from config import BASE_DIR


class Connection:
    def __init__(self):
        self.connection = None
    
    def connect(self):
        if not self.connection:
            self.connection = db.connect(os.path.join(BASE_DIR, 'db/test_db.db'))
        
        cursor = self.connection.cursor()
        
        with open(os.path.join(BASE_DIR, 'db/tables.sql')) as file:
            sql = file.read()
        
        cursor.executescript(sql)
        self.connection.commit()
    
    def close(self):
        self.connection.close()


if __name__ == '__main__':
    with open('tables.sql') as file:
        print(file.read())

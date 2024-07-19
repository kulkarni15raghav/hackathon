import os
import sqlite3

class Database:

    def __init__(self,database_name) -> None:
        self.DATABASE_PATH = f"database/{database_name}.db"


    def create_database(self):

        if not os.path.isfile(self.DATABASE_PATH):
            try:
                conn = sqlite3.connect(self.DATABASE_PATH)

                conn.close()
            
            except:
                print("Database is not created there is some error. Please Verify!!!")

            
    def create_table(self):
        conn = sqlite3.connect(self.DATABASE_PATH)
        cursor = conn.cursor()
        
        with open('sql/create_table.sql', 'r') as sql_file:
            sql_script = sql_file.read()

        cursor.executescript(sql_script)

        conn.commit()
        conn.close()


    def add_visitor(self,first_name,relation,last_name = None):
        conn = sqlite3.connect(self.DATABASE_PATH)
        cursor = conn.cursor()

        cursor.execute("INSERT INTO Frequent_Visitor VALUES (?,?,?,?,?,?)",(1,first_name,last_name,relation,None,None))
        
        conn.commit()
        conn.close()


if __name__ =='__main__':
    db = Database()
    db.create_database('Dementia')
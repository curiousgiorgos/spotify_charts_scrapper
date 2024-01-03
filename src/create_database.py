import sqlite3 
import os 
import shutil
from decouple import config 

DATABASE_LOCATION = config("DATABASE_PATH")
DATABASE_DEV_LOCATION = config("DATABASE_DEV_PATH")
SQL_CREATE_SCRIPT_LOCATION = "sql_scripts/create-owner-objects-1.0.0.0.sql"
SQL_CLEAR_SCRIPT_LOCATION = "sql_scripts/clear-tables.sql"

def run_script_on_db(database, script):
    try:
        conn = sqlite3.connect(database)
        cursor = conn.cursor()
                    
        with open(script, 'r') as script_file:
            sql_script = script_file.read()
            cursor.executescript(sql_script)
        conn.commit()
        conn.close()
    
    except sqlite3.Error as e:
        print(f"Error creating the database: {e}")
        if conn:
            conn.rollback()
        raise
        
def create_database():
    # Check if the database file already exists
    if not os.path.exists(DATABASE_LOCATION):
        try: 
            run_script_on_db(DATABASE_LOCATION, SQL_CREATE_SCRIPT_LOCATION)
            print("Database created successfully.")
        except: 
            if os.path.exists(DATABASE_LOCATION):
                os.remove(DATABASE_LOCATION)
                print("Deleted the incomplete database.")
    # create dev database 
    if not os.path.exists(DATABASE_DEV_LOCATION):
        try:
            shutil.copy2(DATABASE_LOCATION, DATABASE_DEV_LOCATION)
            run_script_on_db(DATABASE_DEV_LOCATION, SQL_CLEAR_SCRIPT_LOCATION)
            print("Dev Database created successfully.")
        except: 
            if os.path.exists(DATABASE_DEV_LOCATION):
                os.remove(DATABASE_DEV_LOCATION)
                print("Deleted the incomplete dev database.")
 
    
if __name__=='__main__':
    create_database()
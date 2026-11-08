import os
import psycopg
from dotenv import load_dotenv
from pathlib import Path
load_dotenv()

PDIR = Path(__file__).resolve().parents[0]
load_dotenv()
FILE_NAME = PDIR / 'script_01.sql'
url = os.getenv('DATABASE_URL','').strip()
print(f"Path directory {PDIR} --- {FILE_NAME}")
print(f"{url}")

with open(FILE_NAME,'r') as file:
    create_table_sql = file.read()
    print(create_table_sql)

    connection = psycopg.connect(url)
    cursor = connection.cursor()
    cursor.execute(create_table_sql)
    connection.commit()
    print("SQL script executed and changes committed successfully.")


"""
class Settings:
   
    def __init__(self):
        self.DATABASE_URL = os.getenv("DATABASE_URL")
        self.SQL_FILE_PATH = os.getenv("SQL_FILE_PATH")
        
        # Validation to ensure required keys exist
        if not self.DATABASE_URL:
            raise ValueError("DATABASE_URL is missing from the configuration settings.")
        if not self.SQL_FILE_PATH:
            raise ValueError("SQL_FILE_PATH is missing from the configuration settings.")

settings = Settings()

connection = None
cursor = None

try:
    with open(settings.SQL_FILE_PATH, 'r') as file:
        create_table_sql = file.read()
    print(f"Successfully read SQL script from {settings.SQL_FILE_PATH}.")

    connection = psycopg2.connect(settings.DATABASE_URL)
    print("Successfully connected to the PostgreSQL database via URL.")

    cursor = connection.cursor()
    cursor.execute(create_table_sql)
    
    connection.commit()
    print("SQL script executed and changes committed successfully.")

except FileNotFoundError:
    print(f"Error: The file '{settings.SQL_FILE_PATH}' was not found. Check your settings.")

except (Exception, psycopg2.DatabaseError) as error:
    if connection:
        connection.rollback()
    print(f"Error while interacting with PostgreSQL: {error}")

finally:
    # 7. Clean up database resources
    if cursor:
        cursor.close()
        print("Cursor closed.")
    if connection:
        connection.close()
        print("PostgreSQL connection is closed.")
"""
import os
import sys
import psycopg
from psycopg.rows import dict_row 
from dotenv import load_dotenv
from pathlib import Path
load_dotenv()

ROOT_DIR = str(Path(__file__).resolve().parents[1])
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)
from app.config import Settings
settings = Settings()

url = settings.database_url
conn=psycopg.connect(url)
cursor = conn.cursor()
# cursor.execute("Select * from users")
# rows = cursor.fetchmany(2)
cursor.execute('SELECT to_regclass(%s)', ('public.chat_messqages',))
table_check = cursor.fetchone()
if table_check:
    print("Yes chat_messages table present")

conn.commit()
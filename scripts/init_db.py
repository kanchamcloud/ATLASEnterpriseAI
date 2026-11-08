import psycopg
from psycopg import sql
from pathlib import Path
import sys
from dotenv import load_dotenv
import os

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / '.env')
SCHEMA = ROOT / 'infra' / 'schema.sql'
REQUIRED = ('documents','feedback','audit_events','approvals','chat_messages')

def main():
    url = os.getenv('DATABASE_URL','').strip()
    if not url or 'YOUR_' in url or 'USERNAME:' in url:
        print('ERROR: Set a real DATABASE_URL in the project .env file.')
        return 1
    if not SCHEMA.is_file():
        print(f'ERROR: Schema not found: {SCHEMA}')
        return 1
    print('Connecting to Render PostgreSQL (credentials hidden)...')
    try:
        with psycopg.connect(url,connect_timeout=15) as conn:
            with conn.transaction():
                conn.execute(SCHEMA.read_text(encoding='utf-8'))
            with conn.cursor() as cur:
                cur.execute('select current_database()')
                dbname = cur.fetchone()[0]
                cur.execute('SELECT to_regclass(%s)', ('public.chat_messages',))
                if cur.fetchone()[0] is None:
                    raise RuntimeError('chat_messages table was not created')
                for table in REQUIRED:
                    cur.execute('SELECT to_regclass(%s)',(f'public.{table}',))
                    if cur.fetchone()[0] is None:
                        raise RuntimeError(f'Missing table: {table}')
        print(f'SUCCESS: Database {dbname!r} initialized; verified {len(REQUIRED)} tables.')
        print('You can safely rerun this script. Existing rows are preserved.')
        return 0

    except Exception as exc:
        print(f'ERROR: Database initialization failed: {type(exc).__name__}: {exc}')
        return 1

if __name__ == '__main__':
    sys.exit(main())

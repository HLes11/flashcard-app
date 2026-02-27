import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    conn = psycopg2.connect(
        host=os.environ.get('DB_HOST', 'localhost'),
        database=os.environ.get('DB_NAME', 'flashcard_db'),
        user=os.environ.get('DB_USER', 'postgres'),
        password=os.environ.get('DB_PASSWORD', 'your_password'),
        port=os.environ.get('DB_PORT', '5432')
    )
    return conn

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    with open('schema.sql', 'r') as f:
        cur.execute(f.read())
    conn.commit()
    cur.close()
    conn.close()

if __name__ == '__main__':
    init_db()
    print("Database initialized successfully!")

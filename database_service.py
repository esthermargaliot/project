import psycopg2
from psycopg2.extras import RealDictCursor

DATABASE_CONFIG = {
    "host": "localhost",
    "database": "your_database_name",
    "user": "your_username",
    "password": "your_password",
}


def execute_sql_query(query: str):
    try:
        conn = psycopg2.connect(**DATABASE_CONFIG)
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute(query)
        if query.strip().lower().startswith("select"):
            result = cursor.fetchall()
        else:
            result = None
            conn.commit()
        cursor.close()
        conn.close()
        return result
    except Exception as e:
        raise Exception(f"Database error: {e}")

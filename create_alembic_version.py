import psycopg2
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# PostgreSQL Database URL
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:root@localhost:5432/article_db"
)

def create_alembic_version():
    conn = psycopg2.connect(DATABASE_URL)
    conn.autocommit = True
    cur = conn.cursor()
    
    try:
        # Drop existing alembic_version table if it exists
        cur.execute("DROP TABLE IF EXISTS alembic_version")
        
        # Create alembic_version table
        cur.execute("""
            CREATE TABLE alembic_version (
                version_num VARCHAR(32) NOT NULL,
                CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
            )
        """)
        print("Created alembic_version table")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    create_alembic_version()

import asyncio
import asyncpg
import sys
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    print("No DATABASE_URL set. Please set it in .env")
    sys.exit(1)

async def fix_db():
    try:
        print("Connecting to database...")
        conn = await asyncpg.connect(DATABASE_URL)
        print("Connected! Terminating all other connections to release locks...")
        
        # Kill all other connections
        await conn.execute('''
            SELECT pg_terminate_backend(pg_stat_activity.pid)
            FROM pg_stat_activity
            WHERE pg_stat_activity.datname = 'railway'
              AND pid <> pg_backend_pid();
        ''')
        print("Other connections terminated.")
        
        await conn.close()
        print("Fix applied successfully.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(fix_db())

from sqlalchemy import create_engine, text
from ..config.settings import DATABASE_URL
import time

def wait_for_db():
    max_retries = 30
    retry_interval = 2

    for i in range(max_retries):
        try:
            engine = create_engine(DATABASE_URL)
            with engine.connect() as connection:
                result = connection.execute(text("SELECT 1"))
                print("Successfully connected to the database!")
                return True
        except Exception as e:
            print(f"Attempt {i + 1}/{max_retries}: Unable to connect to the database. Error: {e}")
            if i < max_retries - 1:
                print(f"Retrying in {retry_interval} seconds...")
                time.sleep(retry_interval)
    
    raise Exception("Could not connect to the database after maximum retries")

if __name__ == "__main__":
    wait_for_db() 
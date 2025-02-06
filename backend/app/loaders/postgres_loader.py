from sqlalchemy import create_engine
import pandas as pd
from ..config.settings import DATABASE_URL

class PostgresLoader:
    def __init__(self):
        self.engine = create_engine(DATABASE_URL)
    
    def load_data(self, df, table_name, if_exists='append'):
        try:
            df.to_sql(
                name=table_name,
                con=self.engine,
                if_exists=if_exists,
                index=False
            )
            print(f"Successfully loaded {len(df)} records to {table_name}")
        except Exception as e:
            print(f"Error loading data to PostgreSQL: {e}") 
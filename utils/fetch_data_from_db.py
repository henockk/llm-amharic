import psycopg2
import pandas as pd

import os
from dotenv import load_dotenv

load_dotenv()

api_token = os.getenv('API_TOKEN')

db_host = os.getenv('DB_HOST')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_name = os.getenv('DB_NAME')
db_port = os.getenv('DB_PORT')


def fetch_data_from_database():
    # Database connection details
    db_details = {
        'dbname': db_name,
        'user': db_user,
        'password': db_password,
        'host': db_host,
        'port': db_port
    }

    # Connect to PostgreSQL
    conn = psycopg2.connect(**db_details)
    
    # Fetch data
    query = "SELECT article FROM cleaned_articles;"
    df = pd.read_sql(query, conn)

    # Close the connection
    conn.close()
    
    return df['article'].tolist()

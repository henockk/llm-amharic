import psycopg2
import pandas as pd

import os
from dotenv import load_dotenv

load_dotenv()

db_host = os.getenv('DB_HOST')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_name = os.getenv('DB_NAME')
db_port = os.getenv('DB_PORT')

conn_params = {
    'dbname': db_name,
    'user': db_user,
    'password': db_password,
    'host': db_host,
    'port': db_port
}


# Define the path to your CSV file
csv_file_path = 'amharic_news.csv'

# Read the CSV file into a pandas DataFrame
df = pd.read_csv(csv_file_path)

# Connect to PostgreSQL
conn = psycopg2.connect(**conn_params)
cur = conn.cursor()

# Create the table
create_table_query = """
CREATE TABLE IF NOT EXISTS articles (
    id SERIAL PRIMARY KEY,
    article TEXT NOT NULL,
    category TEXT NOT NULL
);
"""
cur.execute(create_table_query)
conn.commit()

# Insert data into the table
insert_query = """
INSERT INTO articles (article, category) VALUES (%s, %s)
"""

for _, row in df.iterrows():
    cur.execute(insert_query, (row['article'], row['category']))

conn.commit()

# Close the connection
cur.close()
conn.close()

print("Data loaded successfully")

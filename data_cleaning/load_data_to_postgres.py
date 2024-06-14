import psycopg2
import csv

# Define your PostgreSQL connection parameters
conn_params = {
    'dbname': 'data_warehouse',
    'user': 'postgres',
    'password': 'Mati@1993',
    'host': 'localhost',
    'port': 5432
}

# Function to create table if not exists
def create_table(conn):
    cur = conn.cursor()
    try:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS medical_datas (
                message_id UUID PRIMARY KEY,
                sender_id TEXT,
                message_text TEXT,
                channel TEXT
            )
        """)
        conn.commit()
        print("Table 'medical_datas' created successfully or already exists.")
    except (Exception, psycopg2.DatabaseError) as error:
        conn.rollback()  # Rollback in case of error
        print("Error creating table 'medical_datas':", error)
    finally:
        cur.close()

# Function to load data from CSV and insert into PostgreSQL
def load_data_to_postgres():
    conn = None
    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(**conn_params)

        # Create table if not exists
        create_table(conn)

        cur = conn.cursor()

        # Specify the path to cleaned CSV file
        cleaned_csv_path = './cleaned_data/messages_cleaned.csv'

        # Read data from CSV and insert into medical_datas
        with open(cleaned_csv_path, 'r', newline='', encoding='utf-8') as csvfile:
            csvreader = csv.reader(csvfile)
            next(csvreader)  # Skip header row
            for row in csvreader:
                cur.execute("""
                    INSERT INTO medical_datas (message_id, sender_id, message_text, channel)
                    VALUES (%s, %s, %s, %s)
                """, (row[0], row[1], row[2], row[3]))

        # Commit the transaction
        conn.commit()

        print("Data loaded successfully into PostgreSQL!")

    except (Exception, psycopg2.DatabaseError) as error:
        conn.rollback()  # Rollback in case of error
        print("Error loading data to PostgreSQL:", error)

    finally:
        # Close the cursor and connection
        if conn is not None:
            cur.close()
            conn.close()

if __name__ == "__main__":
    load_data_to_postgres()
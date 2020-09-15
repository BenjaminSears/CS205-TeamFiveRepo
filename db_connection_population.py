import sqlite3
import pandas as pd
from sqlite3 import Error


def get_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print("Error: ", e)

    return conn


def create_table(conn, create_tbl_sql):
    try:
        c = conn.cursor()
        c.execute(create_tbl_sql)
    except Error as e:
        print("Error: ", e)

def main():

    database_file = r"/Users/bensylvester/Desktop/bensylvester/Desktop/pythonProject/CS205_database.db"


    airline_file = r"/Users/bensylvester/Desktop/bensylvester/Desktop/pythonProject/airine_data.csv"

    airline_df = pd.read_csv(airline_file)

    print(airline_df.head())
    create_airline_table_sql = """
    CREATE TABLE IF NOT EXISTS airline (
	airline_id integer PRIMARY KEY,
	name text NOT NULL,
	icao text
    );
    """

    conn = get_connection(database_file)

    if conn is not None:

        create_table(conn, create_airline_table_sql)

    else:
        print("ERROR")
    c = conn.cursor()
    print(c.execute("SELECT * FROM airline"))


main()
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

    database_file = r"/Users/jordanmarchese/PycharmProjects/CS205-TeamFiveRepo/CS205_database.db"


    airline_file = r"/Users/jordanmarchese/PycharmProjects/CS205-TeamFiveRepo/airine.csv"

    route_file = r"/Users/jordanmarchese/PycharmProjects/CS205-TeamFiveRepo/route.csv"

    airline_df = pd.read_csv(airline_file)

    route_df = pd.read_csv(route_file)

    print(airline_df.head())

    print(route_df.head())

    create_airline_table_sql = """
    CREATE TABLE IF NOT EXISTS airline (
	airline_id integer PRIMARY KEY,
	name text NOT NULL,
	icao text
    );
    """

    create_route_table_sql = """
        CREATE TABLE IF NOT EXISTS route (
    	route_id integer PRIMARY KEY,
    	airline text,
    	airline_id integer FOREIGN KEY,
    	source_airport text,
    	source_airport_id integer,
    	destination_airport text,
    	destination_airport_id integer
        );
        """

    conn = get_connection(database_file)

    if conn is not None:

        create_table(conn, create_airline_table_sql)
        create_table(conn, create_route_table_sql)

    else:
        print("ERROR")
    c = conn.cursor()
    print(c.execute("SELECT * FROM airline"))
    print(c.execute("SELECT * FROM route"))


main()
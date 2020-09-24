import sqlite3
import pandas as pd
from sqlite3 import Error
import os.path
from os import path

def connect_to_database():
    conn = None
    try:
        conn = sqlite3.connect("/Users/bensylvester/Desktop/bensylvester/Desktop/CS205-TeamFiveRepo/CS205_database.db")
        return conn

    except Error as e:
        print(e)

        if conn is not None:
            conn.close()


def insert_values_to_table(table_name, csv_file, column_list):
    conn = connect_to_database()

    if conn is not None:
        c = conn.cursor()
        if table_name == "airline":
            c.execute('CREATE TABLE IF NOT EXISTS ' + table_name +
                      '(airline_id        ID,'
                      'name        VARCHAR,'
                      'icao        VARCHAR)')

        if table_name == "route":
            c.execute('CREATE TABLE IF NOT EXISTS ' + table_name +
                      '(route_id                INTEGER,'
                      'airline                  VARCHAR,'
                      'airline_id               INTEGER,'
                      'source_airport           VARCHAR,'
                      'source_airport_id        INTEGER,'
                      'destination_airport      VARCHAR,'
                      'destination_airport_id   INTEGER)')
        df = pd.read_csv(csv_file)
        df.columns = column_list

        df.to_sql(name=table_name, con=conn, if_exists='append', index=False)

        conn.close()
        print('SQL insert process finished')

    else:
        print('Connection to database failed')


def execute_cursor_all_rows(sql_statement):
    conn = connect_to_database()
    c = conn.cursor()
    c.execute(sql_statement)
    return c.fetchall()

def main():
    database_file = "/Users/bensylvester/Desktop/bensylvester/Desktop/CS205-TeamFiveRepo/CS205_database.db"
    airline_csv = "/Users/bensylvester/Desktop/bensylvester/Desktop/CS205-TeamFiveRepo/Airline.csv"
    route_csv = "/Users/bensylvester/Desktop/bensylvester/Desktop/CS205-TeamFiveRepo/Route.csv"

    if path.exists(database_file):
        print(execute_cursor_all_rows("SELECT airline_id FROM airline WHERE name = 'Private flight'"))
        #print(execute_cursor_all_rows("SELECT * FROM route"))
    else:

        airline_column_list = ['airline_id', 'name', 'icao']
        route_column_list = ['route_id', 'airline', 'airline_id', 'source_airport', 'source_airport_id', 'destination_airport', 'destination_airport_id']
        insert_values_to_table("airline", airline_csv, airline_column_list)
        insert_values_to_table("route", route_csv, route_column_list)



main()
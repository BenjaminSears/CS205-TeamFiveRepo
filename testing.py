# WarmUp Project
import csv
import sqlite3
import pandas as pd
from sqlite3 import Error
import os.path
from os import path

def connect_to_database():
    conn = None
    try:
        conn = sqlite3.connect("/Users/bensylvester/Desktop/bensylvester/Desktop/CS205-TeamFiveRepo/CS205_testing.db")
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


def menuOptions():
    # Display options/give user directions
    print("Welcome to the SQL interpreter! If the data is loaded you may input a request. "
          "Or, if it is not loaded you may enter 'Load Data'.\nYou may input 'Help' for our help menu")

    # Prompt user for input
    userInput = input("Please input your request:\n")

    # Check for hard coded inputs 'Help' and 'Load Data'
    if userInput == 'Help' or userInput == 'help':
        helpMenu()

    if userInput == 'Load Data':
        loadData()

    # Parse user's input into a list, seek out keywords

    # parsedUserRequest contains what the user is 'seeking' at index 0, and what they are seeking FOR at index 1
    # Each index is decided based on where the user's comma is place
    # Example input: [Airline ID, 135 Airways]
    # The user is SEEKING Airline ID FOR 135 Airways. Should return 1 as per the Airline.csv
    parsedUserRequest = userInput.split(",")
    airline_column_list = ['airline_id', 'name', 'icao']
    route_column_list = ['route_id', 'airline', 'airline_id', 'source_airport', 'source_airport_id',
                         'destination_airport', 'destination_airport_id']
    for i in range(len(parsedUserRequest)):
        parsedUserRequest[i] = parsedUserRequest[i].strip()

    is_airline_query = False
    is_route_query = False
    if parsedUserRequest[0] in airline_column_list and parsedUserRequest[1] in airline_column_list:
        is_airline_query = True
    if parsedUserRequest[0] in route_column_list and parsedUserRequest[1] in route_column_list:
        is_route_query = True
    if len(parsedUserRequest) == 3:
        if is_airline_query:

            if type(parsedUserRequest[2]) == str:
                sql = "SELECT " + parsedUserRequest[0] + " FROM airline WHERE " + parsedUserRequest[1] + "= '" + parsedUserRequest[2] + "'"
            else:
                sql = "SELECT " + parsedUserRequest[0] + " FROM airline WHERE " + parsedUserRequest[1] + "= " + parsedUserRequest[2]

        if is_route_query:
            if type(parsedUserRequest[2]) == str:
                sql = "SELECT " + parsedUserRequest[0] + " FROM route WHERE " + parsedUserRequest[1] + "= '" + parsedUserRequest[2] + "'"
            else:
                sql = "SELECT " + parsedUserRequest[0] + " FROM route WHERE " + parsedUserRequest[1] + "= " + parsedUserRequest[2]


        #print(sql)
        values = (execute_cursor_all_rows(sql))
        print(set(values))
def helpMenu():
    # Display examples of acceptable queries
    userInput = ""
    while userInput != 'b':
        userInput = input("This is our help menu! Press 'b' to return to the main menu at any time. Below is our syntax for inputs.\n"
                          "The first thing in a statement is what you are SEARCHING followed by a comma. After the comma"
                          " comes the thing you are SEEKING IT FOR.\nExample, if I want the Airline ID for 135 Airways I would input:\n"
                          "[Airline ID, 135 Airways]\nI am SEARCHING for the Airline ID, and I am SEEKING IT FOR 135 Airways\n")
    menuOptions()


def loadData():
    # Load the data from either Route.txt or Airline.txt
    print("Data loaded\n")


# Function reads Airplane and all data in Airplane.txt file
def airplaneCSV():

    '''
    with open('Airline.txt') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                #display Column names
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                #Display rows
                print(f'\t{row[0]}    |     {row[1]}                                 |    {row[2]}.')
                line_count += 1
        print(f'Processed {line_count} lines.')
        '''


# Define methods for grabbing data from the airline dataset

# Retrieve ICAO code based on Airline ID input
def getICAOByID(pAirlineID):
    print("ICAO retrieved by Airline ID")


# Retrieve ICAO code based on Flight Name input
def getICAOByName(pFlightName):
    print("ICAO retrieved by Name")


# Retrieve Airline ID based on ICAO input
def getAirlineIDByICAO(pICAO):
    print("Airline ID retrieved by ICAO")


# Retrieve Airline ID based on Flight Name input
def getAirlineIDByName(pFlightName):
    print("Airline ID retrieved by name")


# Retrieve Flight Name based on Airline ID input
def getFlightNameByID(pAirlineID):
    print("Flight name retrieved by ID")


# Retrieve Flight Name based on ICAO input
def getFlightNameByICAO(pICAO):
    print("Flight name retrieved by ICAO")

# FROM ROUTE.CSV


# Retrieve DestinationAirportID based in Destination Airport input
def getDestinationAirportIDByDestinationAirport(pDestinationAirport):
    print("Destination Airport ID retrieved by Destination Airport")


# Retrieve DestinationAirport based in Destination AirportID input
def getDestinationAirportByDestinationAirportID(pDestinationAirportID):
    print("Destination Airport retrieved by Destination AirportID")


def main():
    menuOptions()


main()

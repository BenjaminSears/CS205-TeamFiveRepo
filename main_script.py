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
          "Or, if it is not loaded you may enter 'Load Data'.\nYou may input 'Help' for our help menu"
          "If your session is complete, please enter 'Q' to exit the interface")

    # Prompt user for input
    userInput = input("Please input your request:\n")
    # Check for hard coded inputs 'Help' and 'Load Data'
    while userInput.upper() != 'Q':
        if userInput.upper() == 'HELP':
            helpMenu()

        if userInput.upper() == 'LOAD DATA':
            loadData()



        # Parse user's input into a list, seek out keywords

        # parsedUserRequest contains what the user is 'seeking' at index 0, and what they are seeking FOR at index 1
        # Each index is decided based on where the user's comma is place
        # Example input: [Airline ID, 135 Airways]
        # The user is SEEKING Airline ID FOR 135 Airways. Should return 1 as per the Airline.csv
        parsedUserRequest = userInput.split(",")
        for i in range(len(parsedUserRequest)):
            parsedUserRequest[i] = parsedUserRequest[i].strip()

        # Hard coded lookups at given indexes

        # Figure out what kind of lookup parsedUserRequest[1] is
        inputIsFlightName = False
        inputIsAirlineID = False
        inputIsICAO = False
        print(parsedUserRequest)
        if len(parsedUserRequest) > 1:
            if len(parsedUserRequest[1]) <= 3:
                try:
                    id = int(parsedUserRequest[1])
                    inputIsAirlineID = True
                except Error as e:
                    break
        
            if len(parsedUserRequest[1]) == 3:
                print(parsedUserRequest[1])
                inputIsICAO = True
                print("TRUE")
            if len(parsedUserRequest[1]) > 3:
                inputIsFlightName = True
        # Find ICAO for a given input
        if parsedUserRequest[0].upper() == 'ICAO':
            if inputIsAirlineID:
                getICAOByID(parsedUserRequest[1])
            if inputIsFlightName:
                getICAOByName(parsedUserRequest[1])

        # Find Airline ID for a given input
        if parsedUserRequest[0] == 'Airline ID':
            if inputIsFlightName:
                getAirlineIDByName(parsedUserRequest[1])
            if inputIsICAO:
                getAirlineIDByICAO(parsedUserRequest[1])

        # Find Name for given input
        if parsedUserRequest[0] == 'Name':
            if inputIsICAO:
                getFlightNameByICAO(parsedUserRequest[1])
            if inputIsAirlineID:
                getFlightNameByID(parsedUserRequest[1])

        # Find Destination Airport ID for given input
        if parsedUserRequest[0] == 'Destination Airport ID':
            getDestinationAirportIDByDestinationAirport(parsedUserRequest[1])

        # Find Destination Airport for given input
        if parsedUserRequest[0] == 'Destination Airport':
            getDestinationAirportByDestinationAirportID(parsedUserRequest[1])


        print("\nThanks for using the SQL interpreter! You may enter another request, or enter 'Q' to quit.\n"
              "Reminder, you can always enter 'Help' for assistance with the interface\n")

        # Prompt user for input
        userInput = input("Please input your request:\n")
        userInput = userInput.lower()
    print("Thanks for using our SQL interpreter, have a nice day!")

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
    # Load the data from either Route.csv or Airline.csv
    database_file = "/Users/bensylvester/Desktop/bensylvester/Desktop/CS205-TeamFiveRepo/CS205_database.db"
    airline_csv = "/Users/bensylvester/Desktop/bensylvester/Desktop/CS205-TeamFiveRepo/Airline.csv"
    route_csv = "/Users/bensylvester/Desktop/bensylvester/Desktop/CS205-TeamFiveRepo/Route.csv"
    if path.exists(database_file):
        print("Data has already been loaded")
    else:

        airline_column_list = ['airline_id', 'name', 'icao']
        route_column_list = ['route_id', 'airline', 'airline_id', 'source_airport', 'source_airport_id',
                             'destination_airport', 'destination_airport_id']
        insert_values_to_table("airline", airline_csv, airline_column_list)
        insert_values_to_table("route", route_csv, route_column_list)

        print("Data loaded\n")
# Define methods for grabbing data from the airline dataset

# Retrieve ICAO code based on Airline ID input
def getICAOByID(pAirlineID):
    sql = "SELECT icao FROM airline WHERE airline_id = " + pAirlineID
    value = execute_cursor_all_rows(sql)
    value_set = set(value)
    print(value_set)

# Retrieve ICAO code based on Flight Name input
def getICAOByName(pFlightName):
    sql = "SELECT icao FROM airline WHERE name = '" + pFlightName + "'"
    print(sql)
    value = execute_cursor_all_rows(sql)
    value_set = set(value)
    print(value_set)

# Retrieve Airline ID based on ICAO input
def getAirlineIDByICAO(pICAO):
    sql = "SELECT airline_id FROM airline WHERE icao = " + pICAO
    print(sql)
    value = execute_cursor_all_rows(sql)
    value_set = set(value)
    print(value_set)


# Retrieve Airline ID based on Flight Name input
def getAirlineIDByName(pFlightName):
    sql = "SELECT airline_id FROM airline WHERE name = '" + pFlightName + "'"
    print(sql)
    value = execute_cursor_all_rows(sql)
    value_set = set(value)
    print(value_set)


# Retrieve Flight Name based on Airline ID input
def getFlightNameByID(pAirlineID):
    sql = "SELECT name FROM airline WHERE airline_id = " + pAirlineID
    print(sql)
    value = execute_cursor_all_rows(sql)
    value_set = set(value)
    print(value_set)


# Retrieve Flight Name based on ICAO input
def getFlightNameByICAO(pICAO):
    sql = "SELECT name FROM airline WHERE icao = '" + pICAO + "'"
    print(sql)
    value = execute_cursor_all_rows(sql)
    value_set = set(value)
    print(value_set)

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
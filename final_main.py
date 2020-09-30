import sqlite3
import pandas as pd
from sqlite3 import Error
from os import path

# global variables must be assigned values
DATABASE_FILE = "/Users/bensylvester/Desktop/bensylvester/Desktop/CS205-TeamFiveRepo/CS205_database.db"
AIRLINE_CSV_FILE = "/Users/bensylvester/Desktop/bensylvester/Desktop/CS205-TeamFiveRepo/Airline.csv"
ROUTE_CSV_FILE = "/Users/bensylvester/Desktop/bensylvester/Desktop/CS205-TeamFiveRepo/Route.csv"

AIRLINE_COLUMN_LIST = ['airline_id', 'name', 'icao']
ROUTE_COLUMN_LIST = ['route_id', 'airline', 'airline_id', 'source_airport', 'source_airport_id',
         'destination_airport', 'destination_airport_id']

def connect_to_database():
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_FILE)
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
            print("CREATING_TABLE: " + table_name)
            c.execute('CREATE TABLE IF NOT EXISTS ' + table_name +
                      '(airline_id        ID,'
                      'name        VARCHAR,'
                      'icao        VARCHAR)')

        if table_name == "route":
            print("CREATING_TABLE: " + table_name)
            c.execute('CREATE TABLE IF NOT EXISTS ' + table_name +
                      '(route_id                INTEGER,'
                      'airline                  VARCHAR,'
                      'airline_id               INTEGER,'
                      'source_airport           VARCHAR,'
                      'source_airport_id        INTEGER,'
                      'destination_airport      VARCHAR,'
                      'destination_airport_id   INTEGER)')
        try:
            df = pd.read_csv(csv_file)
            df.columns = column_list

            df.to_sql(name=table_name, con=conn, if_exists='append', index=False)

            conn.close()
            print('SQL insert process finished for table: ' + table_name)
            return True
        except FileNotFoundError as e:
            print("ERROR: ", e)
            print("Unable to create table: " + table_name)
            return False
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
          "Your database will be loaded if it does not already exist.\nYou may input 'Help' for our help menu"
          "\nIf your session is complete, please enter 'Q' to exit the interface"
          "\n\nREMINDER: please use the corresponding case (upper/lower) for the column the data is representing\n"
          "For example, ICAO codes should always be capitalized, and if you are searching for 'airline_id', make sure that is how you enter it as input\n")
    if not loadData():
        return "ERROR LOADING DATA"
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
        airline_column_list = ['airline_id', 'name', 'icao']
        route_column_list = ['route_id', 'airline', 'airline_id', 'source_airport', 'source_airport_id',
                             'destination_airport', 'destination_airport_id']
        for i in range(len(parsedUserRequest)):
            parsedUserRequest[i] = parsedUserRequest[i].strip()
        sql = ""
        is_airline_query = False
        is_route_query = False
        is_join_query = False
        if parsedUserRequest[0].lower() in airline_column_list and parsedUserRequest[1].lower() in airline_column_list:
            is_airline_query = True
        if parsedUserRequest[0].lower() in route_column_list and parsedUserRequest[1].lower() in route_column_list:
            is_route_query = True
        if parsedUserRequest[0].lower() in airline_column_list and parsedUserRequest[1].lower() not in airline_column_list:
            is_join_query = True
        if parsedUserRequest[0].lower() in route_column_list and parsedUserRequest[1].lower() not in route_column_list:
            is_join_query = True


        if len(parsedUserRequest) == 3:
            if is_airline_query:

                if type(parsedUserRequest[2]) == str:
                    if len(parsedUserRequest[2]) >= 3:
                        sql = "SELECT " + parsedUserRequest[0] + " FROM airline WHERE " + parsedUserRequest[1] + "= '" + \
                              parsedUserRequest[2] + "'"
                    else:
                        sql = "SELECT " + parsedUserRequest[0] + " FROM airline WHERE " + parsedUserRequest[1] + "= '" + \
                              parsedUserRequest[2].upper() + "'"
                else:
                    sql = "SELECT " + parsedUserRequest[0] + " FROM airline WHERE " + parsedUserRequest[1] + "= " + \
                          parsedUserRequest[2]

            if is_route_query:
                if type(parsedUserRequest[2]) == str:
                    sql = "SELECT " + parsedUserRequest[0] + " FROM route WHERE " + parsedUserRequest[1] + "= '" + \
                          parsedUserRequest[2].upper() + "'"
                else:
                    sql = "SELECT " + parsedUserRequest[0] + " FROM route WHERE " + parsedUserRequest[1] + "= " + \
                          parsedUserRequest[2]
            #name, soure_airport_ KZN

            #source_airport, icao, GNL
            if is_join_query and not is_route_query and not is_airline_query:
                if parsedUserRequest[0] in airline_column_list:
                    # if its a string we need qoutes
                    if type(parsedUserRequest[2]) == str:
                        # if its greater than size 3, we dont make it uppercase
                        if len(parsedUserRequest[2]) > 3:
                            sql = "SELECT airline." + parsedUserRequest[0] + " \nFROM airline \nINNER JOIN route ON route.airline_id = airline.airline_id "
                            sql += "AND "
                            if parsedUserRequest[1] in route_column_list and parsedUserRequest[1] not in airline_column_list:
                                sql += "route." + parsedUserRequest[1] + " = '" + parsedUserRequest[2] + "'"
                        # if its equal to size 3 then its an ICAO or code that neeeds to be capitalized
                        if len(parsedUserRequest[2]) == 3:
                            sql = "SELECT airline." + parsedUserRequest[
                                0] + " \nFROM airline \nINNER JOIN route ON route.airline_id = airline.airline_id "
                            sql += "AND "
                            if parsedUserRequest[1] in route_column_list and parsedUserRequest[
                                1] not in airline_column_list:
                                sql += "route." + parsedUserRequest[1] + " = '" + parsedUserRequest[2].upper() + "'"
                    else:
                        sql = "SELECT airline." + parsedUserRequest[0] + " \nFROM airline \nINNER JOIN route ON route.airline_id = airline.airline_id "
                        sql += "AND "
                        if parsedUserRequest[1] in route_column_list and parsedUserRequest[1] not in airline_column_list:
                            sql += "route." + parsedUserRequest[1] + " = " + parsedUserRequest[2]
                if parsedUserRequest[0] in route_column_list:
                    if type(parsedUserRequest[2]) == str:
                        if len(parsedUserRequest[2]) > 3:
                            sql = "SELECT route." + parsedUserRequest[0] + " \nFROM airline \nINNER JOIN route ON route.airline_id = airline.airline_id "
                            sql += "AND "
                            if parsedUserRequest[1] in airline_column_list and parsedUserRequest[1] not in route_column_list:
                                sql += "airline." + parsedUserRequest[1] + " = '" + parsedUserRequest[2] + "'"
                        if len(parsedUserRequest[2]) == 3:
                            sql = "SELECT route." + parsedUserRequest[0] + " \nFROM airline \nINNER JOIN route ON route.airline_id = airline.airline_id "
                            sql += "AND "
                            if parsedUserRequest[1] in airline_column_list and parsedUserRequest[1] not in route_column_list:
                                sql += "airline." + parsedUserRequest[1] + " = '" + parsedUserRequest[2].upper() + "'"
                    else:
                        sql = "SELECT route." + parsedUserRequest[0] + " \nFROM airline \nINNER JOIN route ON route.airline_id = airline.airline_id "
                        sql += "AND "
                        if parsedUserRequest[1] in airline_column_list and parsedUserRequest[1] not in route_column_list:
                            sql += "airline." + parsedUserRequest[1] + " = " + parsedUserRequest[2].upper()

        #print(sql)
        values = set((execute_cursor_all_rows(sql)))
        if len(values) == 0:
            print("You have entered either an invalid request, or none of the data meets the critera you inputted. Please try again")
        else:
            print("Here is the data you have requested:")
            print("Showing the " + parsedUserRequest[0] + " where " + parsedUserRequest[1] + " is equal to " + parsedUserRequest[2] )
            for x in values:
                for data in x:
                    if data is not None:
                        print(parsedUserRequest[0] + ": " + str(data))


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
        print("If you are looking for sample data points to use with our interpreter, enter 'Show Table'\n")
        print("This is our help menu! Press 'b' to return to the main menu at any time. Below is our syntax for inputs.\n"
                          "The first input is what you are SEARCHING FOR, the second is what you are SEARCHING BY "
                          "and the third input is the NAME of what you want to search by. \n\nBelow is an example query of "
                          "searching for the ICAO, by flight name, for 135 Airways. The terminal should display 'GNL'\n"
                          "[ICAO, Name, 135 Airways]\n"
                          "\nIf you are looking to retrieve entries across both tables, we have an option for that. An example of this would be"
                          " inputting \n[source_airport, icao, GNL].\nThis would return the source airports for every entry that has ICAO equal to GNL")

        userInput = input("\n\nHope you found this helpful! Enter 'Show table' to view a table, or enter 'b' to return to our interpreter: ")
        if userInput.lower() == "show table":
            which_table = input("Enter the table you wish to see all data for ('R' for Route and 'A' for Airline) : ")
            if which_table.lower() == 'r':
                sql = "SELECT * FROM route"
                print(ROUTE_COLUMN_LIST)
            if which_table.lower() == 'a':
                sql = "SELECT * FROM airline"
                print(AIRLINE_COLUMN_LIST)
            while which_table.lower() != 'r' and which_table.lower() != 'a':
                which_table = input("Invalid entry. Enter 'R' to view all entries for Route, enter 'A' to view all entries for Airline")
            values = (execute_cursor_all_rows(sql))
            for val in values:
                print(val)
    menuOptions()


def loadData():
    # Load the data from either Route.csv or Airline.csv
    success_load = True
    if path.exists(DATABASE_FILE):
        print("Awesome, your data has already been loaded and your tables have been created")
        return True

    else:


        if not insert_values_to_table("airline", AIRLINE_CSV_FILE, AIRLINE_COLUMN_LIST):
            print("Sorry, you inputted a CSV file that does not exist. Please re-run program to try again")
            success_load = False
        if not insert_values_to_table("route", ROUTE_CSV_FILE, ROUTE_COLUMN_LIST):
            print("Sorry, you inputted a CSV file that does not exist. Please re-run program to try again")
            success_load = False

        if success_load:
            print("Data loaded\n")
            return success_load
        else:
            return success_load

def main():

    menuOptions()


main()
# WarmUp Project
import csv


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
    for i in range(len(parsedUserRequest)):
        parsedUserRequest[i] = parsedUserRequest[i].strip()

    # Hard coded lookups at given indexes

    # Figure out what kind of lookup parsedUserRequest[1] is
    inputIsFlightName = False
    inputIsAirlineID = False
    inputIsICAO = False

    # Find ICAO for a given input
    if parsedUserRequest[0] == 'ICAO':
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

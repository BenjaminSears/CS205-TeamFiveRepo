# WarmUp Project
import csv


def menuOptions():
    # Display options/give user directions
    print("Welcome to the SQL interpreter! If the data is loaded you may input a request. "
          "Or, if it is not loaded you may enter 'Load Data'.")

    # Prompt user for input
    userInput = input("Please input your request:\n")

    # Check for hard coded inputs 'Help' and 'Load Data'
    if userInput == 'Help':
        helpMenu()

    if userInput == 'Load Data':
        loadData()

    # Parse user's input into a list, seek out keywords

    # wordList contains what the user is 'seeking' at index 0, and what they are seeking FOR at index 1
    # Each index is decided based on where the user's comma is place
    # Example input: [Airline ID, 135 Airways]
    # The user is SEEKING Airline ID FOR 135 Airways. Should return 1 as per the Airline.csv
    wordList = userInput.split(",")
    for i in range(len(wordList)):
        wordList[i] = wordList[i].strip()

    # Hard coded lookups at given indexes

    inputIsFlightName = False
    inputIsAirlineID = False
    inputIsICAO = False

    # Find ICAO for a given input
    if wordList[0] == 'ICAO':
        if inputIsAirlineID:
            getICAOByID()

    # Find Airline ID for a given input
    if wordList[0] == 'Airline' and wordList[1] == 'ID':
        print()

    # Find Name for given input
    if wordList[0] == 'Name':
        print()

def helpMenu():
    # Display examples of acceptable queries
    print("Help Menu\n")

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


def main():
    menuOptions()


main()

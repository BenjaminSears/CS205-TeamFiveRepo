#WarmUp Project
import csv


def menuOptions():
    #display options/give user directions
    print("Menu Options:\n")

def helpMenu():
    #Display examples of acceptable queries
    print("Example of Acceptable Queries:\n")


#Function reads Ariplane and all data in Airplane.txt file
def airplaneCSV():
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

def main():
    # call csv file
    print(airplaneCSV())

    # call menuOptions
    print(menuOptions())

    # call helpMenu
    print(helpMenu())

main()
#Jared Staman
#
#CS 423 Project 1
#The following code reads in applicant data and selects applications that meet certain criteria

import csv

def main():

    with open('applicants.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter= ',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')




main()

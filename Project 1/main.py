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
                #print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                applicant = [row[0], row[1], row[2], row[3], row[4], row[5]]
                decision = analyze_applicant4(applicant)
                print(decision)
                #need to add to results.csv


def analyze_applicant1(applicant):
    #average above 85
    average = int(applicant[0]) + int(applicant[1]) + int(applicant[2]) + int(applicant[3]) + int(applicant[4]) + int(applicant[5])
    average = average / 5
    
    if average > 85:
        decision = "ACCEPT"
    else:
        decision = "REJECT"

    return decision
    


def analyze_applicant2(applicant):
    #no grade below 65
    for score in range(len(applicant)):
        if int(applicant[score]) < 65:
            decision = "REJECT"
            return decision
    
    decision = "ACCEPT"
    return decision


def analyze_applicant3(applicant):
    #at least 4 grades above 85
    count = 0
    for score in range(len(applicant)):
        if int(applicant[score]) > 85:
            count += 1

    if count > 3:
        decision = "ACCEPT"
    else:
        decision = "REJECT"

    return decision

def analyze_applicant4(applicant):
    #average above 85 in the 5 CS classes
    average = int(applicant[0]) + int(applicant[1]) + int(applicant[2]) + int(applicant[3]) + int(applicant[4])
    average = average / 4

    if average > 85:
        decision = "ACCEPT"
    else:
        decision = "REJECT"

    return decision


main()

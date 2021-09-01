#Jared Staman
#
#CS 423 Project 1
#The following code reads in applicant data and selects applications that meet certain criteria

import csv

def main():

    with open('applicants.csv') as csv_file:
        with open('results.csv', 'w') as results:
        #read from applicants.csv  
            csv_reader = csv.reader(csv_file, delimiter= ',')
            csv_writer = csv.writer(results, delimiter= ' ')
            line_count = 0
            for row in csv_reader:
                #ignore header
                if line_count == 0:
                    line_count += 1
                else:
                    applicant = [row[0], row[1], row[2], row[3], row[4], row[5]]
                    decision1 = analyze_applicant1(applicant)
                    decision2 = analyze_applicant2(applicant)
                    decision3 = analyze_applicant3(applicant)
                    decision4 = analyze_applicant4(applicant)
                    
                    #must be accepted in all 4 application analyses
                    if(decision1 == "ACCEPT"):
                        if(decision1 == decision2 and decision2 == decision3 and decision3 == decision4 and decision4 == decision1):
                            decision = decision1
                        else:
                            decision = "REJECT"
                    else:
                        decision = "REJECT"
        
                    csv_writer.writerow([decision])
                        
        


def analyze_applicant1(applicant):
    #average above 85 in all classes including non CS class
    average = int(applicant[0]) + int(applicant[1]) + int(applicant[2]) + int(applicant[3]) + int(applicant[4]) + int(applicant[5])
    average = average / 6
    
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
    #at least 4 grades above 85 including non CS class
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
    average = average / 5

    if average > 85:
        decision = "ACCEPT"
    else:
        decision = "REJECT"

    return decision


main()

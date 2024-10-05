import csv
import argparse
import os
from email.message import EmailMessage
from email.mime.text import MIMEText
import smtplib
from mentor import Mentor
from mentee import Mentee

def main():
    parser = argparse.ArgumentParser(description = 'Automation of mentor-mentee introduction emails')
    parser.add_argument('input_file', type = str, help = 'Path to the input CSV file containing mentor and mentee matches')

    args = parser.parse_args()
    inputFile = args.input_file

    mentorDict = {}

    with open(inputFile, 'r') as file:
        next(file)  

        reader = csv.reader(file, delimiter=',', quotechar='"')

        for row in reader:
            mentorName, menteeName, mentorEmail, menteeEmail, mentorGrade, menteeGrade, mentorClassInterest, menteeClassInterest, mentorResearchInterest, menteeResearchInterest, mentorIndustryInterest, menteeIndustryInterest, mentorGradSchoolInterest, menteeGradSchoolInterest, mentorMajorPivotInterest, menteeMajorPivotInterest = row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15]
            mentee = Mentee(menteeName, menteeEmail, menteeGrade, menteeClassInterest, menteeResearchInterest, menteeIndustryInterest, menteeGradSchoolInterest, menteeMajorPivotInterest)
            if mentorName in mentorDict:
                mentorDict[mentorName].addMentee(mentee)
            else: 
                mentor = Mentor(mentorName, mentorEmail, mentorGrade, mentorClassInterest, mentorResearchInterest, mentorIndustryInterest, mentorGradSchoolInterest, mentorMajorPivotInterest, [mentee])
                mentorDict[mentorName] = mentor

        print(mentorDict)

    for key, value in mentorDict.items():
        message = f"Hi {key},\n\n My name is Airi and I'm the mentorship chair for Tufts CSX. Thank you for expressing interest in being a mentor for the CSX mentorship program. We're excited to release mentorship pairings for this upcoming year! \n\n"
        for mentee in value.getMentees():
            message = message + f"You've been matched with:\n{mentee.getName()}. \nEmail: {mentee.getEmail()}. \nGrade: {mentee.getGrade()}\nInterest in being mentored about the following subjects: What classes to take for the CS major: {mentee.getClassInterest()}, CS research: {mentee.getResearchInterest()}, CS industry: {mentee.getIndustryInterest()}, CS graduate school: {mentee.getGradInterest()}, Pivoting to/from the CS major: {mentee.getPivotInterest()}.\n\n"
        message = message + "We are hosting an event this upcoming Monday October 7th from 12-1 in JCC 170 for mentors and mentees to meet. Snacks will be provided! Please reach out to your mentee(s) to plan if you will meet at this event. The exact format of this mentorship will be up to you and your mentee(s); however, it is recommended that you organize several informal conversations/coffee chats throughout the semester. Please reach out with any questions, concerns, or if you’d like to pick up an additional mentee!"

        pswd = os.environ["EMAIL_PASSWORD"]
        FROM = os.environ["EMAIL_ADDRESS"]
        TO = value.getEmail()
        SUBJECT = "CSX Mentorship program matches"
        TEXT = message

        email = EmailMessage()
        email["From"] = FROM
        email["To"] = TO
        email["Subject"] = SUBJECT
        email.set_content(TEXT)

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(FROM, pswd)
        server.sendmail(FROM, TO, email.as_string())
        server.close()
            
if __name__ == '__main__':
    main()

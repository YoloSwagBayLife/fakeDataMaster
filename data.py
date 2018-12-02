import random
import time
import os
import sys
import shutil

# these are all external modules you'll need to download
# note: faker is installed via pip as "fake-factory" at the moment
import requests
from faker import Factory
from faker.providers import job
from tempmail import TempMail
from simplejson import scanner
from bs4 import BeautifulSoup
from shutil import copyfile

fake = Factory.create('en_US')
donatedTo = [x.replace('\n', '') for x in open('./donatedTo.txt').readlines()]
majors = [x.replace('\n', '') for x in open('./majorSelection.txt').readlines()]
school = [x.replace('\n', '') for x in open('./schools.txt').readlines()]
activity = [x.replace('\n', '') for x in open('./activities.txt').readlines()]
workPlace = [x.replace('\n', '') for x in open('./companies.txt').readlines()]

if len(sys.argv) > 142:
    times = int(sys.fargv[1])
else:
    times = 10
for attempt in range(times):
    # Creation of Alumni Schema + GradInfo Schema
    alumniSSN = random.randint(11100000, 999999999)
    alumniFname, alumniLname = fake.first_name(), fake.last_name()
    alumniPhoneNumber = '(' + str(random.choice(['410', '443', '301'])) + ')' + str(random.randint(111,999)) + '-' + str(random.randint(0000,9999))
    # every email created is directly created from the Alumni's name
    alumniEmail = alumniFname[0].lower() + alumniLname.lower() + str(random.randint(0, 99)).zfill(2) + '@mail.com'
    alumniNumFamily = random.randint(0, 4)
    alumniDeadAlive = str(random.choice(['T', 'F', 'F', 'F', 'F', 'T', 'F', 'F', 'F', 'F', 'F', 'F']))
    # alumniAge is only used for age of the spouse / children
    alumniAge = random.randint(24, 99)

    alumniGPA = random.randrange(239, 401)/100
    alumniMajor = random.choice(majors)
    alumniMinor = random.choice(majors)
    alumniYear = 2018-random.randint(1, 75)
    alumniSchool = random.choice(school)

    # Creation of Spouse Schema, assuming that if there is only 1 direct family member, it is a spouse
    spouseSSN = str(random.randint(11100000, 999999999))
    spouseFname = fake.first_name()
    spouseAge = alumniAge + random.randint(-6, 6)

    # Creation of children is done in the text file creation, only way I can get a variable number of children created

    # Creation of Contact Report Schema
    contactDate = fake.date_time_between('-10y', '-1y')
    contactWhoContacted = random.choice([alumniFname, spouseFname])
    contactDonated = str(random.choice(['T', 'F', 'F', 'F', 'F']))

    # Creation of Donation History is done in text file creation, and is only
    # created if the Contact Report donated is true

    # Creation of Involvement Schema
    involvementYears = random.randint(1, 4)
    activityname = random.choice(activity)

    # Creation of Job, WorkAs, Workplace and WorksAt schema
    fake = Factory.create()
    fake.add_provider(job)

    positionTitle = fake.job()
    jobID = random.randint(123, 84923)
    salary = random.randrange(15000, 150000, 1000)
    companyName = random.choice(workPlace)
    companyAddress = fake.address()
    formattedCompanyAddress = companyAddress.replace('\r', '').replace('\n', '')
    companyPhone = '(' + str(random.randint(100, 900)) + ')' + str(random.randint(111,999)) + '-' + str(random.randint(0000,9999))

    with open('alumni.txt', 'a') as textFile:
        textFile.write("New Alumni Information:\n")
        textFile.write("Alumni(%s, %s, %s, %s, %s, %d, %s)" %
        (alumniSSN, alumniFname, alumniLname, alumniEmail, alumniPhoneNumber, alumniNumFamily, alumniDeadAlive) + "\n")
        textFile.write("GradInfo(%s, %s, %s, %s, %s)" % (alumniSSN, alumniGPA, alumniMajor, alumniMinor, alumniSchool) + "\n")
        textFile.write("Involvement(%s, %s, %s)" % (alumniSSN, activityname, involvementYears) + "\n")
        if alumniNumFamily >= 1:
            textFile.write("Spouse(%s, %s, %s, %s)" % (spouseSSN, spouseFname, spouseAge, alumniSSN) + "\n")
        for childAttempt in range(alumniNumFamily - 1):
            childSSN = str(random.randint(11100000, 999999999))
            childFname = fake.first_name()
            childAge = (alumniAge - 24 + random.randint(0, 6))
            textFile.write("Children(%s, %s, %s, %s)" % (childSSN, childFname, childAge, alumniSSN) + "\n")
        textFile.write("ContactReport(%s, %s, %s)" % (contactDate, contactWhoContacted, contactDonated) + "\n")
        if contactDonated == 'T':
            dateDonated = fake.date_time_between(contactDate, 'now')
            donationAmount = random.randrange(100, 5000, 10)
            donatedToSchool = random.choice(donatedTo)
            textFile.write("DonationHistry(%s, %s, %s, %s)" % (dateDonated, donationAmount, donatedToSchool, alumniSSN) + "\n")
        textFile.write("Job(%s, %s,)" % (positionTitle, salary) + "\n")
        textFile.write("WorkAs(%s, %s, %s)" % (positionTitle, salary, alumniSSN) + "\n")
        textFile.write("Workplace(%s, %s, %s)" % (companyName, formattedCompanyAddress, companyPhone) + "\n")
        textFile.write("WorksAt(%s, %s, %s)" % (companyName, formattedCompanyAddress, alumniSSN) + "\n\n")

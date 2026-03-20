# File: voter_analytics/models.py
# Author: Yash Kedia (yashkedi@bu.edu), 3/19/26
# Description: Models for voter_analytics application

from django.db import models
import datetime
import csv

# Create your models here.
class Voter(models.Model):
    '''
    Store/represent the data from one voter in the town of Newton, MA
    '''

    #identification
    voter_id = models.TextField()
    last_name = models.TextField()
    first_name = models.TextField()
    street_num = models.IntegerField(null=True, blank=True)  # optional: some addresses have no street number
    street_name = models.TextField()
    apt_num = models.CharField(max_length=10, null=True, blank=True)  # optional: not all voters have an apt
    zip = models.CharField(max_length=10)
    dob = models.DateField(null=True, blank=True)  # null allowed for records missing birth date
    date_registration = models.DateField(null=True, blank=True)  # null allowed for older registrations
    party = models.CharField(max_length=2, null=True, blank=True)  # e.g. 'D', 'R', 'U' (unenrolled)
    precinct = models.CharField(max_length=10, null=True, blank=True)  # voting precinct within Newton

    #voting info — one boolean per election; True means the voter participated
    v20 = models.BooleanField(null=True, blank=True)        # 2020 general election
    v21town = models.BooleanField(null=True, blank=True)    # 2021 town election
    v21primary = models.BooleanField(null=True, blank=True) # 2021 primary election
    v22 = models.BooleanField(null=True, blank=True)        # 2022 general election
    v23 = models.BooleanField(null=True, blank=True)        # 2023 general election

    voter_score = models.IntegerField()  # count of elections participated in (0–5)

    def __str__(self):
        '''Return a string representation of this model instance.'''
        return f'{self.first_name} {self.last_name} ({self.voter_id}, {self.dob}), {self.voter_score}'
    
def load_data():
    '''
    Function to load data records from CSV file into Django model instances.
    '''
    filename = 'voter_analytics/newton_voters.csv'
    f = open(filename)
    f.readline()  # discard the header row so it isn't parsed as a record

    for line in f:
        fields = line.split(',')  # CSV columns map directly to Voter fields by index
        try:
            def parse_bool(x):
                # CSV stores booleans as the string 'TRUE'/'FALSE'
                return x.strip().upper() == 'TRUE'

            voter = Voter(
                voter_id=fields[0],       # column 0: unique voter ID
                last_name=fields[1],      # column 1: last name
                first_name=fields[2],     # column 2: first name
                street_num=int(fields[3]),# column 3: street number
                street_name=fields[4],    # column 4: street name
                apt_num=fields[5],        # column 5: apartment number (may be empty)
                zip=fields[6],            # column 6: zip code
                dob=fields[7],            # column 7: date of birth (YYYY-MM-DD)
                date_registration=fields[8],  # column 8: registration date
                party=fields[9].strip(),  # column 9: strip whitespace from party code
                precinct=fields[10],      # column 10: precinct
                v20=parse_bool(fields[11]),       # column 11: voted in 2020
                v21town=parse_bool(fields[12]),   # column 12: voted in 2021 town
                v21primary=parse_bool(fields[13]),# column 13: voted in 2021 primary
                v22=parse_bool(fields[14]),       # column 14: voted in 2022
                v23=parse_bool(fields[15]),       # column 15: voted in 2023
                voter_score=int(fields[16])       # column 16: total elections participated in
            )

            voter.save()  # persist the new Voter record to the database
            print(f"Created voter: {voter}")

        except:
            print(f"Skipped: {fields}")  # skip malformed rows (e.g. missing fields)

    print(f"Done. Created {Voter.objects.count()} voters.")
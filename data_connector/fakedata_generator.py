import pandas as pd
from faker import Faker
from datetime import date, timedelta
import random

def generate_fakedata_badges(num_rows = 1000):
    fake = Faker()
    schema = {
        "GUI": [fake.random_int(min=10000, max=99999) for _ in range(num_rows)],
        "BadgeID": [fake.random_int(min=1000, max=9999) for _ in range(num_rows)],
        "BadgeType": [random.choice(["Platinum", "Gold", "Silver", "Bronze"]) for _ in range(num_rows)],
        "BadgeStatus": [random.choice(["Active", "Inactive"]) for _ in range(num_rows)],
        "Domain": [random.choice(["IT", "Finance", "HR", "Marketing", "Data Strategy"]) for _ in range(num_rows)],
        "InitiateaBadgeDate": [fake.date_between(start_date="-1y", end_date="today") for _ in range(num_rows)],
        "EmployeeStatus": [random.choice(["Active", "Inactive"]) for _ in range(num_rows)],
        "RankName": [random.choice(["Manager", "Director", "Employee", "Supervisor"]) for _ in range(num_rows)],
        "Service_Line": [random.choice(["TAX", "Consulting", "IT", "Audit", "RMS"]) for _ in range(num_rows)],
        "SubSL": [random.choice(["SubSL_1", "SubSL_2", "SubSL_3"]) for _ in range(num_rows)],
        "Country": [random.choice(["USA", "Canada", "UK"]) for _ in range(num_rows)],
        "City": [random.choice(["New York", "Los Angeles", "London", "Toronto"]) for _ in range(num_rows)],
        "Badge Title": [random.choice(["AI001", "BI002", "TAX01", "DS02"]) for _ in range(num_rows)],
        "Pillar": [random.choice(["Business", "Technology", "Leadership", None]) for _ in range(num_rows)],
    }

    # Create a DataFrame
    df = pd.DataFrame(schema)
    df["BadgeEarnedDate"] = [
        fake.date_between(start_date=date.today() - timedelta(days=365), end_date=date.today())
        for _ in range(num_rows)
    ]

    return df

def generate_fakedata_workforce(num_rows = 1000):
    # Initialize the Faker object
    fake = Faker()
    df = pd.DataFrame()

    # Generate data for additional headers
    df["Rank Description"] = [fake.sentence() for _ in range(num_rows)]
    df["Business Title"] = [fake.job() for _ in range(num_rows)]
    df["Experience Level"] = [random.choice(["Entry Level", "Mid Level", "Senior Level"]) for _ in range(num_rows)]
    df["Activity Type Description"] = [fake.sentence() for _ in range(num_rows)]
    df["BU Description"] = [fake.company_suffix() for _ in range(num_rows)]
    df["OU Description"] = [fake.catch_phrase() for _ in range(num_rows)]
    df["MU Description"] = [fake.catch_phrase() for _ in range(num_rows)]
    df["SMU Description"] = [fake.catch_phrase() for _ in range(num_rows)]
    df["Service Line (SL Level 1)"] = [random.choice(["ServiceLine1", "ServiceLine2", "ServiceLine3"]) for _ in range(num_rows)]
    df["Sub Service Line (SL Level 2)"] = [random.choice(["SubSL1", "SubSL2", "SubSL3"]) for _ in range(num_rows)]
    df["Management Area (BU Level 1)"] = [fake.company() for _ in range(num_rows)]
    df["Management Region (BU Level 2)"] = [fake.city() for _ in range(num_rows)]
    df["Location City"] = [fake.city() for _ in range(num_rows)]
    df["Location Country"] = [random.choice(["USA", "Canada", "UK"]) for _ in range(num_rows)]
    df["Employee Status"] = [random.choice(["Active", "Inactive"]) for _ in range(num_rows)]
    df["Active Status"] = [random.choice(["Active", "Inactive"]) for _ in range(num_rows)]
    df["Full Part Time"] = [random.choice(["Full-Time", "Part-Time"]) for _ in range(num_rows)]
    df["Standard Hours"] = [fake.random_int(min=30, max=40) for _ in range(num_rows)]
    df["Overtime Eligibility"] = [random.choice(["Eligible", "Not Eligible"]) for _ in range(num_rows)]
    df["Regular Temporary"] = [random.choice(["Regular", "Temporary"]) for _ in range(num_rows)]
    df["Employee Type"] = [random.choice(["Type1", "Type2", "Type3"]) for _ in range(num_rows)]
    df["EY Start Date"] = [fake.date_between(start_date="-10y", end_date="-1y") for _ in range(num_rows)]
    df["Last Rehire Date"] = [fake.date_between(start_date="-5y", end_date="-1y") for _ in range(num_rows)]
    df["Company Seniority Date"] = [fake.date_between(start_date="-10y", end_date="-1y") for _ in range(num_rows)]
    df["Current Length of Service"] = [fake.random_int(min=1, max=10) for _ in range(num_rows)]
    df["Total EY Length of Service"] = [fake.random_int(min=1, max=10) for _ in range(num_rows)]
    df["Last Promotion Date"] = [fake.date_between(start_date="-5y", end_date="-1y") for _ in range(num_rows)]
    df["Last Progression Date"] = [fake.date_between(start_date="-5y", end_date="-1y") for _ in range(num_rows)]
    df["Department Code"] = [fake.random_int(min=100, max=999) for _ in range(num_rows)]
    df["Source"] = [random.choice(["Source1", "Source2", "Source3"]) for _ in range(num_rows)]
    df["Language Preference"] = [random.choice(["English", "French", "Spanish"]) for _ in range(num_rows)]
    df["Gender"] = [random.choice(["Male", "Female", "Other"]) for _ in range(num_rows)]
    df["Date Of Birth"] = [fake.date_of_birth(minimum_age=21, maximum_age=60) for _ in range(num_rows)]
    df["Age"] = [date.today().year - dob.year for dob in df["Date Of Birth"]]
    df["GUI"] = [fake.uuid4() for _ in range(num_rows)]
    df["CounsellorGUI"] = [fake.uuid4() for _ in range(num_rows)]
    df["Service_Line"] = [random.choice(["ServiceLine1", "ServiceLine2", "ServiceLine3"]) for _ in range(num_rows)]
    df["Record_Start_Date"] = [fake.date_between(start_date="-1y", end_date="today") for _ in range(num_rows)]

    return df


def upload_to_sqlitedb():
    pass
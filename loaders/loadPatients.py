import pandas as pd

def load(conn, file1="./data/csv/patients.csv", **kwargs):
    df = pd.read_csv(file1)
    df["DEATHDATE"] = df["DEATHDATE"].fillna("2999-12-31 00:00:00")
    df = df.fillna('')
    attributes = {
        "FirstName": "FIRST",
        "LastName": "LAST",
        "Prefix": "PREFIX",
        "Suffix": "SUFFIX",
        "MaidenName": "MAIDEN",
        "Gender": "GENDER",
        "Race": "RACE",
        "Ethnicity": "ETHNICITY",
        "SSN": "SSN",
        "DL": "DRIVERS",
        "Passport": "PASSPORT",
        "DateOfBirth": "BIRTHDATE",
        "DateOfDeath": "DEATHDATE"
    }
    numUpserted = conn.upsertVertexDataFrame(df, "Patient", "Id", attributes)
    print("Upserted "+str(numUpserted)+" Patients")

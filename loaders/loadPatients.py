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
        "SSN": "SSN",
        "DL": "DRIVERS",
        "Passport": "PASSPORT",
        "DateOfBirth": "BIRTHDATE",
        "DateOfDeath": "DEATHDATE"
    }
    numUpserted = conn.upsertVertexDataFrame(df, "Patient", "Id", attributes)
    print("Upserted "+str(numUpserted)+" Patients")

    numUpserted = conn.upsertVertexDataFrame(df, "Gender", "GENDER", attributes={})
    print("Upserted", str(numUpserted), "Genders")

    numUpserted = conn.upsertVertexDataFrame(df, "Race", "RACE", attributes={})
    print("Upserted", str(numUpserted), "Races")

    numUpserted = conn.upsertVertexDataFrame(df, "Ethnicity", "ETHNICITY", attributes={})
    print("Upserted", str(numUpserted), "Ethnicities")

    numUpserted = conn.upsertEdgeDataFrame(df, "Patient", "patientRace", "Race", from_id="Id", to_id="RACE", attributes={})
    numUpserted = conn.upsertEdgeDataFrame(df, "Patient", "patientGender", "Gender", from_id="Id", to_id="GENDER", attributes={})
    numUpserted = conn.upsertEdgeDataFrame(df, "Patient", "patientEthnicity", "Ethnicity", from_id="Id", to_id="ETHNICITY", attributes={})



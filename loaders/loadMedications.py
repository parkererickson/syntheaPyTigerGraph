import pandas as pd

def load(conn, file1="./data/csv/medications.csv", **kwargs):
    df = pd.read_csv(file1)
    df["CODE"] = df["CODE"].astype(str)
    df["REASONCODE"] = df["REASONCODE"].astype(str)
    df["STOP"] = df["STOP"].fillna("2999-12-31 00:00:00")
    df["Id"] = df["ENCOUNTER"].str.cat(df["CODE"], sep=":")
    df = df.fillna('')
    attributes = {
        "Code": "CODE",
        "Description": "DESCRIPTION",
        "Cost": "BASE_COST",
        "Dispense": "DISPENSES",
        "TotalCost": "TOTALCOST",
        "ReasonCode": "REASONCODE",
        "ReasonDescription": "REASONDESCRIPTION"
    }
    numUpserted = conn.upsertVertexDataFrame(df, "Medication", "Id", attributes)
    print("Upserted "+str(numUpserted)+" Medications")

    attributes = {
        "Started": "START",
        "Stopped": "STOP"
    }

    numUpserted = conn.upsertEdgeDataFrame(df, "Patient", "hasMedication", "Medication", from_id="PATIENT", to_id="Id", attributes=attributes)
    print("Upserted "+str(numUpserted)+" hasMedication edges")

    attributes = {
        "Code": "REASONCODE",
        "Description": "REASONDESCRIPTION"
    }

    numUpserted = conn.upsertVertexDataFrame(df, "SnomedCode", "REASONCODE", attributes)

    numUpserted = conn.upsertEdgeDataFrame(df, "Medication", "reasonOfMedication", "SnomedCode", from_id="Id", to_id="REASONCODE", attributes={})

    attributes = {
        "Code": "CODE",
        "Description": "DESCRIPTION"
    }

    numUpserted = conn.upsertVertexDataFrame(df, "SnomedCode", "CODE", attributes)

    numUpserted = conn.upsertEdgeDataFrame(df, "Medication", "medicationCode", "SnomedCode", from_id="Id", to_id="CODE", attributes={})

    numUpserted = conn.upsertEdgeDataFrame(df, "Medication", "prescribedAt", "Visit", from_id="Id", to_id="ENCOUNTER", attributes={})
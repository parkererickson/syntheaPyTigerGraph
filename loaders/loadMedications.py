import pandas as pd

def load(conn, file1="/Users/pericks4/syntheaPyTigerGraph/data/csv/medications.csv", **kwargs):
    df = pd.read_csv(file1)
    df["CODE"] = df["CODE"].astype(str)
    df["REASONCODE"] = df["REASONCODE"].astype(str)
    df["STOP"] = df["STOP"].fillna("2999-12-31 00:00:00")
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
    numUpserted = conn.upsertVertexDataFrame(df, "Medication", "CODE", attributes)
    print("Upserted "+str(numUpserted)+" Medications")

    attributes = {
        "Started": "START",
        "Stopped": "STOP"
    }

    numUpserted = conn.upsertEdgeDataFrame(df, "Patient", "hasMedication", "Medication", from_id="PATIENT", to_id="CODE", attributes=attributes)
    print("Upserted "+str(numUpserted)+" hasCondition edges")
import pandas as pd

def load(conn, file1="./data/csv/conditions.csv", **kwargs):
    df = pd.read_csv(file1)
    df["CODE"] = df["CODE"].astype(str)
    df["STOP"] = df["STOP"].fillna("2999-12-31 00:00:00")
    df["Condition"] = "Condition"
    attributes = {
        "Code": "CODE",
        "Description": "DESCRIPTION",
        "CodeType": "Condition"
    }
    numUpserted = conn.upsertVertexDataFrame(df, "SnomedCode", "CODE", attributes)
    print("Upserted "+str(numUpserted)+" Conditions")

    attributes = {
        "Started": "START",
        "Stopped": "STOP"
    }

    numUpserted = conn.upsertEdgeDataFrame(df, "Patient", "hasCondition", "SnomedCode", from_id="PATIENT", to_id="CODE", attributes=attributes)
    print("Upserted "+str(numUpserted)+" hasCondition edges")
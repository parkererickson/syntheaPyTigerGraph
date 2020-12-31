import pandas as pd

def load(conn, file1="./data/csv/conditions.csv", **kwargs):
    df = pd.read_csv(file1)
    df["CODE"] = df["CODE"].astype(str)
    df["STOP"] = df["STOP"].fillna("2999-12-31 00:00:00")
    attributes = {
        "Code": "CODE",
        "Description": "DESCRIPTION",

    }
    numUpserted = conn.upsertVertexDataFrame(df, "Condition", "CODE", attributes)
    print("Upserted "+str(numUpserted)+" Conditions")

    attributes = {
        "Started": "START",
        "Stopped": "STOP"
    }

    numUpserted = conn.upsertEdgeDataFrame(df, "Patient", "hasCondition", "Condition", from_id="PATIENT", to_id="CODE", attributes=attributes)
    print("Upserted "+str(numUpserted)+" hasCondition edges")
import pandas as pd

def load(conn, file1="/Users/pericks4/syntheaPyTigerGraph/data/csv/careplans.csv", **kwargs):
    df = pd.read_csv(file1)
    df["CODE"] = df["CODE"].astype(str)
    df["REASONCODE"] = df["REASONCODE"].astype(str)
    df["STOP"] = df["STOP"].fillna("2999-12-31 00:00:00")
    df = df.fillna('')
    attributes = {
        "Code": "CODE",
        "Description": "DESCRIPTION",
        "Started": "START",
        "Stopped": "STOP",
        "ReasonCode": "REASONCODE",
        "ReasonDescription": "REASONDESCRIPTION",

    }
    numUpserted = conn.upsertVertexDataFrame(df, "CarePlan", "Id", attributes)
    print("Upserted "+str(numUpserted)+" CarePlans")

    numUpserted = conn.upsertEdgeDataFrame(df, "Patient", "hasCarePlan", "CarePlan", from_id="PATIENT", to_id="Id", attributes={})
    print("Upserted "+str(numUpserted)+" hasCarePlan edges")
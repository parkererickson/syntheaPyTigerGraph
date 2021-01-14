import pandas as pd

def load(conn, file1="./data/csv/careplans.csv", **kwargs):
    #Id,START,STOP,PATIENT,ENCOUNTER,CODE,DESCRIPTION,REASONCODE,REASONDESCRIPTION
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

    attributes = {
        "Code": "REASONCODE",
        "Description": "REASONDESCRIPTION"
    }

    numUpserted = conn.upsertVertexDataFrame(df, "SnomedCode", "REASONCODE", attributes)

    numUpserted = conn.upsertEdgeDataFrame(df, "CarePlan", "reasonOfCarePlan", "SnomedCode", from_id="Id", to_id="REASONCODE", attributes={})

    attributes = {
        "Code": "CODE",
        "Description": "DESCRIPTION"
    }

    numUpserted = conn.upsertVertexDataFrame(df, "SnomedCode", "CODE", attributes)

    numUpserted = conn.upsertEdgeDataFrame(df, "CarePlan", "carePlanCode", "SnomedCode", from_id="Id", to_id="CODE", attributes={})

    numUpserted = conn.upsertEdgeDataFrame(df, "CarePlan", "recommendedAt", "Visit", from_id="Id", to_id="ENCOUNTER", attributes={})
import pandas as pd

#DATE,PATIENT,ENCOUNTER,CODE,DESCRIPTION,BASE_COST,REASONCODE,REASONDESCRIPTION

def load(conn, file1="./data/csv/procedures.csv", **kwargs):
    df = pd.read_csv(file1)
    df["CODE"] = df["CODE"].astype(str)
    df["REASONCODE"] = df["REASONCODE"].astype(str)
    df = df.fillna('')
    attributes = {
        "Code": "CODE",
        "Description": "DESCRIPTION",
        "Cost": "BASE_COST",
        "ReasonCode": "REASONCODE",
        "ReasonDescription": "REASONDESCRIPTION"
    }
    numUpserted = conn.upsertVertexDataFrame(df, "PatientProcedure", "CODE", attributes)
    print("Upserted "+str(numUpserted)+" PatientProcedures")

    attributes = {
        "Performed": "DATE",
    }

    numUpserted = conn.upsertEdgeDataFrame(df, "Patient", "hasProcedure", "PatientProcedure", from_id="PATIENT", to_id="CODE", attributes=attributes)
    print("Upserted "+str(numUpserted)+" hasProcedure edges")
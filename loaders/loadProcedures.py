import pandas as pd

#DATE,PATIENT,ENCOUNTER,CODE,DESCRIPTION,BASE_COST,REASONCODE,REASONDESCRIPTION

def load(conn, file1="./data/csv/procedures.csv", **kwargs):
    df = pd.read_csv(file1)
    df["CODE"] = df["CODE"].astype(str)
    df["REASONCODE"] = df["REASONCODE"].astype(str)
    df["Id"] = df["ENCOUNTER"].str.cat(df["CODE"], sep=":")
    df = df.fillna('')
    attributes = {
        "Code": "CODE",
        "Description": "DESCRIPTION",
        "Cost": "BASE_COST",
        "ReasonCode": "REASONCODE",
        "ReasonDescription": "REASONDESCRIPTION"
    }
    numUpserted = conn.upsertVertexDataFrame(df, "PatientProcedure", "Id", attributes)
    print("Upserted "+str(numUpserted)+" PatientProcedures")

    attributes = {
        "Performed": "DATE",
    }

    numUpserted = conn.upsertEdgeDataFrame(df, "Patient", "hasProcedure", "PatientProcedure", from_id="PATIENT", to_id="Id", attributes=attributes)
    print("Upserted "+str(numUpserted)+" hasProcedure edges")


    attributes = {
        "Code": "REASONCODE",
        "Description": "REASONDESCRIPTION"
    }

    numUpserted = conn.upsertVertexDataFrame(df, "SnomedCode", "REASONCODE", attributes)

    numUpserted = conn.upsertEdgeDataFrame(df, "PatientProcedure", "reasonOfProcedure", "SnomedCode", from_id="Id", to_id="REASONCODE", attributes={})

    attributes = {
        "Code": "CODE",
        "Description": "DESCRIPTION"
    }

    numUpserted = conn.upsertVertexDataFrame(df, "SnomedCode", "CODE", attributes)

    numUpserted = conn.upsertEdgeDataFrame(df, "PatientProcedure", "procedureCode", "SnomedCode", from_id="Id", to_id="CODE", attributes={})

    numUpserted = conn.upsertEdgeDataFrame(df, "PatientProcedure", "tookPlaceAt", "Visit", from_id="Id", to_id="ENCOUNTER", attributes={})
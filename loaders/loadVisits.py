import pandas as pd

def load(conn, file1="./data/csv/encounters.csv", **kwargs):
    df = pd.read_csv(file1)
    df["CODE"] = df["CODE"].astype(str)
    attributes = {
        "Code": "CODE",
        "Description": "DESCRIPTION",
        "Started": "START",
        "Stopped": "STOP",
        "Cost": "TOTAL_CLAIM_COST"
    }
    numUpserted = conn.upsertVertexDataFrame(df, "Visit", "Id", attributes)
    print("Upserted "+str(numUpserted)+" Visits")

    numUpserted = conn.upsertEdgeDataFrame(df, "Patient", "patientVisit", "Visit", from_id="PATIENT", to_id="Id", attributes={})
    print("Upserted "+str(numUpserted)+" patientVisit edges")

    numUpserted = conn.upsertEdgeDataFrame(df, "Provider", "providerVisit", "Visit", from_id="PROVIDER", to_id="Id", attributes={})
    print("Upserted "+str(numUpserted)+" providerVisit edges")
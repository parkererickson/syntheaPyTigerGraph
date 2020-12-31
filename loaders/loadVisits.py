import pandas as pd

def load(conn, file1="/Users/pericks4/syntheaPyTigerGraph/data/csv/encounters.csv", **kwargs):
    df = pd.read_csv(file1)
    df = df.sample(frac=.25) # Sample 25% of visits
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
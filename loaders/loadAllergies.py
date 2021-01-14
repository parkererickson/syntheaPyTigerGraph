import pandas as pd

def load(conn, file1="./data/csv/allergies.csv", **kwargs):
    df = pd.read_csv(file1)
    df["Allergy"] = "Allergy"
    attributes = {
        "Description": "DESCRIPTION",
        "CodeType": "Allergy"
    }
    numUpserted = conn.upsertVertexDataFrame(df, "SnomedCode", "CODE", attributes)
    print("Upserted "+str(numUpserted)+" Allergies")

    df["STOP"] = df["STOP"].fillna("2999-12-31 00:00:00")
    attributes = {
        "Started": "START",
        "Stopped": "STOP"
    }

    numUpserted = conn.upsertEdgeDataFrame(df, "Patient", "hasAllergy", "SnomedCode", from_id="PATIENT", to_id="CODE", attributes={})
    print("Upserted "+str(numUpserted)+" hasAllergy edges")
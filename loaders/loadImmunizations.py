import pandas as pd

def load(conn, file1="./data/csv/immunizations.csv", **kwargs):
    df = pd.read_csv(file1)
    df["CODE"] = df["CODE"].astype(str)
    df["DATE"] = df["DATE"].fillna("2999-12-31 00:00:00")
    df["Immunization"] = "Immunization"
    attributes = {
        "Code": "CODE",
        "Description": "DESCRIPTION",
        "CodeType": "Immunization"
    }
    numUpserted = conn.upsertVertexDataFrame(df, "SnomedCode", "CODE", attributes)
    print("Upserted "+str(numUpserted)+" Immunizations")

    attributes = {
        "Performed": "DATE"
    }

    numUpserted = conn.upsertEdgeDataFrame(df, "Patient", "hasImmunization", "SnomedCode", from_id="PATIENT", to_id="CODE", attributes=attributes)
    print("Upserted "+str(numUpserted)+" hasImmunization edges")
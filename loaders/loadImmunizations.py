import pandas as pd

def load(conn, file1="/Users/pericks4/syntheaPyTigerGraph/data/csv/immunizations.csv", **kwargs):
    df = pd.read_csv(file1)
    df["CODE"] = df["CODE"].astype(str)
    df["DATE"] = df["DATE"].fillna("2999-12-31 00:00:00")
    attributes = {
        "Code": "CODE",
        "Description": "DESCRIPTION",
        "Cost": "BASE_COST"
    }
    numUpserted = conn.upsertVertexDataFrame(df, "Immunization", "CODE", attributes)
    print("Upserted "+str(numUpserted)+" Immunizations")

    attributes = {
        "Performed": "DATE"
    }

    numUpserted = conn.upsertEdgeDataFrame(df, "Patient", "hasImmunization", "Immunization", from_id="PATIENT", to_id="CODE", attributes=attributes)
    print("Upserted "+str(numUpserted)+" hasImmunization edges")
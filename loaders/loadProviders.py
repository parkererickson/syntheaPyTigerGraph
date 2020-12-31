import pandas as pd

def load(conn, file1="./data/csv/providers.csv", **kwargs):
    df = pd.read_csv(file1)
    attributes = {
        "Name": "NAME",
        "Gender": "GENDER",
        "Speciality": "SPECIALITY",
        "Utilization": "UTILIZATION"
    }
    numUpserted = conn.upsertVertexDataFrame(df, "Provider", "Id", attributes)
    print("Upserted "+str(numUpserted)+" Providers")

    numUpserted = conn.upsertEdgeDataFrame(df, "Provider", "worksAt", "Organization", from_id="Id", to_id="ORGANIZATION", attributes={})
    print("Upserted "+str(numUpserted)+" worksAt edges")

import pandas as pd

#Id,NAME,ADDRESS,CITY,STATE,ZIP,LAT,LON,PHONE,REVENUE,UTILIZATION

def load(conn, file1="./data/csv/organizations.csv", **kwargs):
    df = pd.read_csv(file1)
    attributes = {
        "Name": "NAME",
        "Utilization": "UTILIZATION",
    }
    numUpserted = conn.upsertVertexDataFrame(df, "Organization", "Id", attributes)
    print("Upserted "+str(numUpserted)+" Organizations")
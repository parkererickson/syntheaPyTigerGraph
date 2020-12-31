import pandas as pd

#DATE,PATIENT,ENCOUNTER,CODE,DESCRIPTION,VALUE,UNITS,TYPE

def load(conn, file1="./data/csv/observations.csv", **kwargs):
    df = pd.read_csv(file1)
    df = df.fillna('')
    df["CODE"] = df["CODE"].astype(str)
    df["VALUE"] = df["VALUE"].astype(str)
    attributes = {
        "Code": "CODE",
        "Description": "DESCRIPTION",
    }
    numUpserted = conn.upsertVertexDataFrame(df, "Observation", "CODE", attributes)
    print("Upserted "+str(numUpserted)+" Observations")

    attributes = {
        "Performed": "DATE",
        "Measurement": "VALUE",
        "Units": "UNITS",
        "ValueType": "VALUE"
    }

    numUpserted = conn.upsertEdgeDataFrame(df, "Patient", "hasObservation", "Observation", from_id="PATIENT", to_id="CODE", attributes=attributes)
    print("Upserted "+str(numUpserted)+" hasObservation edges")
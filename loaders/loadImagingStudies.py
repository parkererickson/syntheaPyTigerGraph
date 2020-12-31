import pandas as pd

def load(conn, file1="./data/csv/imaging_studies.csv", **kwargs):
    df = pd.read_csv(file1)
    df["BODYSITE_CODE"] = df["BODYSITE_CODE"].astype(str)
    df["MODALITY_CODE"] = df["MODALITY_CODE"].astype(str)
    df["SOP_CODE"] = df["SOP_CODE"].astype(str)
    attributes = {
        "BodySiteCode": "BODYSITE_CODE",
        "BodySiteDescription": "BODYSITE_DESCRIPTION",
        "ModalityCode": "MODALITY_CODE",
        "ModalityDescription": "MODALITY_DESCRIPTION",
        "SOPCode": "SOP_CODE",
        "SOPDescription": "SOP_DESCRIPTION",
        "ImagingDate": "DATE"
    }
    numUpserted = conn.upsertVertexDataFrame(df, "ImagingStudy", "Id", attributes)
    print("Upserted "+str(numUpserted)+" ImagingStudies")

    attributes = {
        "Performed": "DATE"
    }

    numUpserted = conn.upsertEdgeDataFrame(df, "Patient", "hasImagingStudy", "ImagingStudy", from_id="PATIENT", to_id="Id", attributes=attributes)
    print("Upserted "+str(numUpserted)+" hasImagingStudy edges")
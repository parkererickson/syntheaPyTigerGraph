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

    attributes = {
        "Code": "BODYSITE_CODE",
        "Description": "BODYSITE_DESCRIPTION"
    }

    numUpserted = conn.upsertVertexDataFrame(df, "SnomedCode", "BODYSITE_CODE", attributes)

    numUpserted = conn.upsertEdgeDataFrame(df, "ImagingStudy", "imagingBodyCode", "SnomedCode", from_id="Id", to_id="BODYSITE_CODE", attributes={})

    attributes = {
        "Code": "SOP_CODE",
        "Description": "SOP_DESCRIPTION"
    }

    numUpserted = conn.upsertVertexDataFrame(df, "SnomedCode", "SOP_CODE", attributes)

    numUpserted = conn.upsertEdgeDataFrame(df, "ImagingStudy", "imagingSOPCode", "SnomedCode", from_id="Id", to_id="SOP_CODE", attributes={})

    attributes = {
        "Code": "MODALITY_CODE",
        "Description": "MODALITY_DESCRIPTION"
    }

    numUpserted = conn.upsertVertexDataFrame(df, "SnomedCode", "MODALITY_CODE", attributes)

    numUpserted = conn.upsertEdgeDataFrame(df, "ImagingStudy", "imagingModalityCode", "SnomedCode", from_id="Id", to_id="MODALITY_CODE", attributes={})

    numUpserted = conn.upsertEdgeDataFrame(df, "ImagingStudy", "imagedAt", "Visit", from_id="Id", to_id="ENCOUNTER", attributes={})
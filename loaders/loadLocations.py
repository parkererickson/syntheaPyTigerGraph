import pandas as pd

# Orgs: Id,NAME,ADDRESS,CITY,STATE,ZIP,LAT,LON,PHONE,REVENUE,UTILIZATION
# Pats: Id,BIRTHPLACE,ADDRESS,CITY,STATE,COUNTY,ZIP,LAT,LON

def load(conn, file1="./data/csv/organizations.csv", file2="./data/csv/organizations.csv", **kwargs):
    orgs = pd.read_csv(file1)
    pats = pd.read_csv(file2)

    # Load State, City, Zip Vertices
    attr = {
        "Name": "STATE"
    }
    conn.upsertVertexDataFrame(orgs, "State", "STATE", attr)
    conn.upsertVertexDataFrame(pats, "State", "STATE", attr)

    attr = {
        "Name": "CITY"
    }
    conn.upsertVertexDataFrame(orgs, "City", "CITY", attr)
    conn.upsertVertexDataFrame(pats, "City", "CITY", attr)

    attr = {
        "ZipCode": "ZIP",
        "Latitude": "LAT",
        "Longitude": "LON"
    }
    conn.upsertVertexDataFrame(orgs, "Zip", "ZIP", attr)
    conn.upsertVertexDataFrame(pats, "Zip", "ZIP", attr)

    # Load State, City, Zip Edges
    conn.upsertEdgeDataFrame(orgs, "Zip", "zipInState", "State", from_id="ZIP", to_id="STATE", attributes={})
    conn.upsertEdgeDataFrame(pats, "Zip", "zipInState", "State", from_id="ZIP", to_id="STATE", attributes={})

    conn.upsertEdgeDataFrame(orgs, "Zip", "zipInCity", "City", from_id="ZIP", to_id="CITY", attributes={})
    conn.upsertEdgeDataFrame(pats, "Zip", "zipInCity", "City", from_id="ZIP", to_id="CITY", attributes={})

    conn.upsertEdgeDataFrame(orgs, "City", "cityInState", "State", from_id="CITY", to_id="STATE", attributes={})
    conn.upsertEdgeDataFrame(pats, "City", "cityInState", "State", from_id="CITY", to_id="STATE", attributes={})
    
    # Load Location Vertex
    attr = {
        "Latitude": "LAT",
        "Longitude": "LON"
    }
    conn.upsertVertexDataFrame(orgs, "Location", "Id", attr)
    conn.upsertVertexDataFrame(pats, "Location", "Id", attr)

    # Load patientLocatedAt and organizationLocatedAt edges
    conn.upsertEdgeDataFrame(orgs, "Organization", "organizationLocatedAt", "Location", from_id="Id", to_id="Id", attributes={})
    conn.upsertEdgeDataFrame(pats, "Patient", "patientLocatedAt", "Location", from_id="Id", to_id="Id", attributes={})

    # Load Addresses
    attr = {
        "Name": "ADDRESS"
    }
    conn.upsertVertexDataFrame(orgs, "Address", "ADDRESS", attr)
    conn.upsertVertexDataFrame(pats, "Address", "ADDRESS", attr)

    # Load Address Edges
    conn.upsertEdgeDataFrame(pats, "Patient", "residesAt", "Address", from_id="Id", to_id="ADDRESS", attributes={})
    conn.upsertEdgeDataFrame(pats, "Address", "addressInZip", "Zip", from_id="ADDRESS", to_id="ZIP", attributes={})
    conn.upsertEdgeDataFrame(orgs, "Organization", "foundAt", "Address", from_id="Id", to_id="ADDRESS", attributes={})
    conn.upsertEdgeDataFrame(orgs, "Address", "addressInZip", "Zip", from_id="ADDRESS", to_id="ZIP", attributes={})
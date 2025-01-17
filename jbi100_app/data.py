import plotly.express as px
import pandas as pd
import numpy as np
import re
from jbi100_app.config import int_to_month
#Note from Dembis: If ewe want to modify the data before it is used in the visualizations, 
# it might be a good idea to do it beforehand and upload a 2nd file to the project if it takes a long time to process

def get_data():
    # Read data
    file = "ASI_Database.xlsx"
    df = pd.read_excel(file)
    df = treat_data(df)
    df["Number_of_fatal_incidents"] = df["Victim.injury"].apply(
    lambda x: 1 if isinstance(x, str) and "fatal" in x.lower() else 0
    )
    return df

def treat_data(df):
    df['Injury.category'] = df['Injury.location'].apply(lambda loc: categorize_injury_location(loc))
    df['Month'] = df['Incident.month'].apply(lambda loc: int_to_month(loc))
    df = make_lower_case(df, 'Site.category')
    df = make_lower_case(df, 'Victim.injury')
    df = jitter_coordinates(df)
    return df
    
def categorize_injury_location(location):
    if pd.isna(location):
        return 'Unknown'
    location = location.lower()
    if re.search(r'leg|thigh|calf|ankle|knee', location):
        return 'Leg'
    elif re.search(r'foot', location):
        return 'Foot'
    elif re.search(r'arm|hand|wrist|shoulder|elbow', location):
        return 'Arm'
    elif re.search(r'head|face|neck', location):
        return 'Head/Neck'
    elif re.search(r'torso|chest|abdomen|back', location):
        return 'Torso'
    elif re.search(r'other: uninjured', location):
        return 'Uninjured'
    return 'Other'

def make_lower_case(df, column):
    df[column] = df[column].astype(str).str.lower()
    return df

#Jitter the coordinates to avoid overlapping points
def jitter_coordinates(df, jitter_amount=0.05):
    # Ensure Longitude and Latitude are numeric
    df["Longitude"] = pd.to_numeric(df["Longitude"], errors="coerce")
    df["Latitude"] = pd.to_numeric(df["Latitude"], errors="coerce")

    # Identify duplicated coordinates
    duplicated_coords = df.duplicated(subset=["Longitude", "Latitude"], keep=False)
    df_jittered = df.copy()

    # Apply jitter only to duplicated points
    df_jittered.loc[duplicated_coords, "Longitude"] += np.random.uniform(
        -jitter_amount, jitter_amount, size=duplicated_coords.sum()
    )
    df_jittered.loc[duplicated_coords, "Latitude"] += np.random.uniform(
        -jitter_amount, jitter_amount, size=duplicated_coords.sum()
    )

    return df_jittered

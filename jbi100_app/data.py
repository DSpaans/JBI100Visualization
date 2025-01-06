import plotly.express as px
import pandas as pd
#Note from Dembis: If ewe want to modify the data before it is used in the visualizations, 
# it might be a good idea to do it beforehand and upload a 2nd file to the project if it takes a long time to process


def get_dummy_data():
    # Read data
    df = px.data.iris()

    # Any further data preprocessing can go her

    return df

def get_data():
    # Read data
    file = "..jbi100_app/ASI_Database.xlsx"
    df = pd.read_excel(file)
    return df
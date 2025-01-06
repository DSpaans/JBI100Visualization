import plotly.express as px
import pandas as pd
import re
#Note from Dembis: If ewe want to modify the data before it is used in the visualizations, 
# it might be a good idea to do it beforehand and upload a 2nd file to the project if it takes a long time to process


def get_dummy_data():
    # Read data
    df = px.data.iris()
    return df

def get_data():
    # Read data
    file = "ASI_Database.xlsx"
    df = pd.read_excel(file)
    df = treat_data(df)
    return df

def treat_data(df):
    return df
    


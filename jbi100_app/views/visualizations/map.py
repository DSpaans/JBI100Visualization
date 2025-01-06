#Make Map of australia visualization here
from dash import dcc, html
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

class ScatterMap(html.Div):
    def __init__(self, name, feature_x, feature_y, df):
        self.html_id = name.lower().replace(" ", "-")
        self.df = df
        self.feature_x = feature_x
        self.feature_y = feature_y

        # Equivalent to `html.Div([...])`
        super().__init__(
            className="graph_card",
            children=[
                html.H6(name),
                dcc.Graph(id=self.html_id)
            ],
        )

    def update(self):
        self.fig = go.Figure()

        # Create map
        fig = px.scatter_geo(self.df, lat="Latitude", lon="Longitude", color="Country",
                             hover_name="Country", size="Population", projection="natural earth")

        self.fig = fig
        return self.fig
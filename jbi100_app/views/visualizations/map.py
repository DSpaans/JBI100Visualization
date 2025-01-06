#Make Map of australia visualization here
from dash import dcc, html
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

class ScatterGeo(html.Div):
    def __init__(self, name, df, feature_x):
        self.html_id = name.lower().replace(" ", "-")
        self.df = df
        self.feature_x = feature_x

        # Equivalent to `html.Div([...])`
        super().__init__(
            className="graph_card",
            children=[
                html.H6(name),
                dcc.Graph(id=self.html_id, figure=self.update())
            ],
        )

    def update(self):
        self.fig = go.Figure(data=go.Scattergeo(
            lon = self.df['Longitude'],
            lat = self.df['Latitude'],
            text = self.df['Location'],
            mode = 'markers',
            marker=dict(
                    color='blue',   # Change marker color as needed
                    size=6)
            )
        )

        self.fig.update_layout(
            title = 'Australian Shark Incidents',
            geo=dict(
                scope='world', 
                center=dict(lat=-28, lon=133), # roughly central Australia
                projection_scale=2.5,         # controls zoom level
                showland=True,
                landcolor='rgb(217, 217, 217)',
                )
        )
        return self.fig
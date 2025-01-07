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
            style={"display": "flex", "justifyContent": "center", "height": "100%"},
            children=[
                html.H6(name),
                dcc.Graph(id=self.html_id, figure=self.update(),
                style={'height': '600px', 'width': '100%'}
                )
            ],
        )

    #Update the map with original dataset of the filtered dataset
    def update(self, filtered_df=None):
        #If there is no filtered_df, default to self.df
        if filtered_df is None:
            filtered_df = self.df

        #Build the figure
        fig = go.Figure(data=go.Scattergeo(
            lon = filtered_df['Longitude'],
            lat = filtered_df['Latitude'],
            text = filtered_df['Location'],
            mode = 'markers',
            marker=dict(
                    color='blue',   # Change marker color as needed
                    opacity=0.7,
                    size=8)
            )
        )

        fig.update_layout(
            title = '', #Removed title as it is already in the card from the app.py file
            title_x = 0.5,
            geo=dict(
                scope='world', 
                center=dict(lat=-28, lon=133), # roughly central Australia
                projection_scale=2.5,         # controls zoom level
                showland=True,
                landcolor='rgb(217, 217, 217)',
                ),
                margin=dict(l=10, r=10, t=40, b=10)
        )
        return fig
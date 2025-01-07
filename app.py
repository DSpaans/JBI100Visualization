from jbi100_app.main import app
from jbi100_app.data import get_data
from jbi100_app.views.menu import make_menu_layout
from jbi100_app.views.visualizations.map import ScatterGeo
from jbi100_app.views.visualizations.scatterplot import Scatterplot
from jbi100_app.views.visualizations.heatmap import Heatmap

from dash import html, dcc
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output

if __name__ == '__main__':
    
    df = get_data()

    # Instantiate custom views
    scatter_map_aus = ScatterGeo("Incidents Map", df, 'Junk_for_now')
    heatmap = Heatmap("Heatmap", df)

    #scatterplot1 = Scatterplot("Scatterplot 1", 'sepal_length', 'sepal_width', df)
    #scatterplot2 = Scatterplot("Scatterplot 2", 'petal_length', 'petal_width', df)

    # Note from Dembis: We can use the menu.py file to create a modular dashboard layout over here
    app.layout = html.Div(
        id="app-container",
        children=[
            # Left column
            html.Div(
                id="left-column",
                className="three columns",
                children=make_menu_layout(df)
            ),

            # Right column
            html.Div(
                id="right-column",
                className="nine columns",
                children=[
                    #Map Visualization
                    scatter_map_aus,
                    #Heatmap
                    heatmap
                ],
            ),
        ],
    )

    # Define interactions   
    @app.callback(
        Output(heatmap.html_id, "figure"), [
        Input("year-slider", "value")
    ])
    def update_heatmap(year_range):
        low, high = year_range
        filtered_df = df[df["Incident.year"].between(low, high)]
        return heatmap.update(filtered_df)
    
    @app.callback(
        Output(scatter_map_aus.html_id, "figure"), [
        Input("year-slider", "value")
    ])
    def update_map(year_range):
        low, high = year_range
        filtered_df = df[df["Incident.year"].between(low, high)]
        return scatter_map_aus.update(filtered_df)
    
    app.run_server(debug=True, dev_tools_ui=False)
    
"""    @app.callback(
        Output(scatterplot1.html_id, "figure"), [
        Input("select-color-scatter-1", "value"),
        Input(scatterplot2.html_id, 'selectedData')
    ])
    def update_scatter_1(selected_color, selected_data):
        return scatterplot1.update(selected_color, selected_data)

    @app.callback(
        Output(scatterplot2.html_id, "figure"), [
        Input("select-color-scatter-2", "value"),
        Input(scatterplot1.html_id, 'selectedData')
    ])
    def update_scatter_2(selected_color, selected_data):
        return scatterplot2.update(selected_color, selected_data)"""

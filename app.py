from jbi100_app.main import app
from jbi100_app.data import get_data
from jbi100_app.views.menu import make_menu_layout, make_time_slider
from jbi100_app.views.visualizations.map import ScatterGeo
from jbi100_app.views.visualizations.scatterplot import Scatterplot
from jbi100_app.views.visualizations.heatmap import Heatmap
from jbi100_app.views.visualizations.barchart import BarChart
from jbi100_app.views.visualizations.radarplot import RadarPlot
from jbi100_app.config import column_options_1, column_options_heatmap, column_options_barchart
from dash import html, dcc
from dash.dependencies import Input, Output

if __name__ == '__main__':
    
    df = get_data()

    # Instantiate custom views
    scatter_map_aus = ScatterGeo("Incidents Map", df, 'Junk_for_now')
    heatmap = Heatmap("Heatmap", df)
    barchart = BarChart("Bar Chart", df)
    radar_plot = RadarPlot("Shark Radar Plot", df)

    app.layout = html.Div(
        id="app-container",
        children=[
            # Left column
            html.Div(
                id="left-column",
                className="three columns",
                children=make_menu_layout(df, column_options_1, column_options_heatmap, column_options_barchart),
                style={
                    "position": "fixed",
                    "top": "0",
                    "left": "0",
                    "bottom": "0",
                    "width": "25%",
                    "padding": "10px",
                    "background-color": "#f8f9fa",
                    "overflow": "auto",
                }
            ),

            # Middle column
            html.Div(
                id="middle-column",
                className="nine columns",
                children=[
                    #Map Visualization
                    scatter_map_aus,
                    #Heatmap
                    heatmap,
                    #Barchart
                    barchart,
                    #Radar Plot
                    radar_plot
                ],
                style={
                    "width": "70%",
                    "margin-left": "25%",
                    "padding": "10px",
                    "overflow": "auto",
                }
            ),

            # Right column
            html.Div(
                id="range-slider-container",
                className="one columns",
                children=[make_time_slider(df)],
                style={
                    "position": "fixed",
                    "bottom": "0",
                    "right": "0",
                    "width": "5%",
                    "height": "100%",
                    "padding": "5px",
                    "background-color": "#f8f9fa",
                    "overflow": "auto",
                },
                ),
        ],
    )

    # Define interactions   
    
    # def update_heatmap(year_range):
    #     low, high = year_range
    #     filtered_df = df[df["Incident.year"].between(low, high)]
    #     return heatmap.update(filtered_df)
    
    # @app.callback(
    #     Output(scatter_map_aus.html_id, "figure"),
    #     Input("select-hover-column", "value"),
    # )
    
    # def update_map(year_range, selected_column):
    #     low, high = year_range
    #     filtered_df = df[df["Incident.year"].between(low, high)]
    #     return scatter_map_aus.update(filtered_df, selected_column)
    
    @app.callback(
        [Output(scatter_map_aus.html_id, "figure"), Output(heatmap.html_id, "figure"), Output(barchart.html_id, "figure"), Output(radar_plot.html_id, "figure")],
        [Input("year-slider", "value"), Input("select-hover-column", "value"), 
         Input("select-x-heatmap", "value"), Input("select-y-heatmap", "value"),
         Input("select-x-bar", "value"), Input("select-y-bar", "value"),
         Input("select-radar-shark-type", "value")],
    )
    
    def update_visualizations(year_range, selected_column, selected_x, selected_y, x_bar, y_bar, selected_shark_type):
        # Filter data based on the year range
        low, high = year_range
        filtered_df = df[df["Incident.year"].between(low, high)]

        # Update the map
        map_figure = scatter_map_aus.update(filtered_df, selected_column)
        # Update the heatmap
        heatmap_figure = heatmap.update(selected_x, selected_y, filtered_df)
        # Update the barchart
        barchart_figure = barchart.update(x_bar, y_bar, filtered_df)
        # Update the radarplot
        radar_figure = radar_plot.update(selected_shark_type, filtered_df)

        return map_figure, heatmap_figure, barchart_figure, radar_figure
    
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

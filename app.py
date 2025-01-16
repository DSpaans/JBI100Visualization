from jbi100_app.main import app
from jbi100_app.data import get_data
from jbi100_app.views.menu import make_menu_layout, make_time_slider
from jbi100_app.views.visualizations.map import ScatterGeo
from jbi100_app.views.visualizations.heatmap import Heatmap
from jbi100_app.views.visualizations.barchart import BarChart
from jbi100_app.views.visualizations.radarplot import RadarPlot
from jbi100_app.views.visualizations.histogram import Histogram
from jbi100_app.config import column_options_heatmap, column_options_barchart
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.graph_objects as go

if __name__ == '__main__':
    
    df = get_data()

    global_min_length = df["Shark.length.m"].min(skipna=True)
    global_max_length = df["Shark.length.m"].max(skipna=True)
    global_min_depth = df["Depth.of.incident.m"].min(skipna=True)
    global_max_depth = df["Depth.of.incident.m"].max(skipna=True)

    # Instantiate custom views
    scatter_map_aus = ScatterGeo("Incidents Map", df)
    heatmap = Heatmap("Heatmap", df)
    barchart = BarChart("Bar Chart", df)
    radar_plot = RadarPlot("Shark Radar Plot", df, global_min_length, global_max_length, global_min_depth, global_max_depth)
    time_hist = Histogram(name=None, df=df, show_title=False)

    app.layout = html.Div(
        id="app-container",
        children=[
            # Left column
            html.Div(
                id="left-column",
                className="three columns",
                children=make_menu_layout(df, column_options_heatmap, column_options_barchart, time_hist),
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
                    html.Div(
                        style={"display": "flex"},
                        children=[
                            html.Div(
                                scatter_map_aus,
                                style={
                                    "width": "50%",
                                    "padding": "0px",
                                    "margin-right": "5px"
                                }
                            ),
                            html.Div(
                                radar_plot,
                                style={
                                    "width": "50%",
                                    "padding": "0px",
                                    "margin-left": "5px"
                                }
                            ),
                        ],
                    ),
                    #Heatmap
                    heatmap,
                    #Barchart
                    barchart,
                ],
                style={
                    "width": "74%",
                    "margin-left": "26%",
                    "padding": "10px",
                    "overflow": "auto",
                }
            ),

        ],
    )

    # Define interactions      
    @app.callback(
        [Output(scatter_map_aus.html_id, "figure"),
         Output(heatmap.html_id, "figure"),
         Output(barchart.html_id, "figure"),
         Output(radar_plot.html_id, "figure"),
         Output(time_hist.html_id, "figure"),
         Output("select-state", "options"),
         Output("select-shark", "options")],
        [Input("year-slider", "value"), 
         Input("select-state", "value"), 
         Input("select-shark", "value"), 
         Input("select-x-heatmap", "value"), 
         Input("select-y-heatmap", "value"),
         Input("select-x-bar", "value"), 
         Input("select-y-bar", "value"), 
         Input(scatter_map_aus.html_id, "selectedData")],
    )
    
    def update_visualizations(year_range, selected_state, selected_shark, 
                              x_heat, y_heat, x_bar, y_bar, map_selected_data):
        # Extract year range
        low, high = year_range
        
        # df to keep track of non selected datapoints in the map
        partial_for_map = df[df["Incident.year"].between(low, high)].copy()
        # df for the states dropdown
        partial_states = df[df["Incident.year"].between(low, high)]
        # df for the sharks dropdown    
        partial_sharks = df[df["Incident.year"].between(low, high)]
        # df for the histogram   
        final_histo = df.copy()
        # Final filtered df to be used in the visualizations            
        final_df = df[df["Incident.year"].between(low, high)]

        # If the user has picked a specific State, limit partial_sharks to that state
        if selected_state != "All states":
            partial_for_map = partial_for_map[partial_for_map["State"] == selected_state]
            partial_sharks = partial_sharks[partial_sharks["State"] == selected_state]
            final_histo = final_histo[final_histo["State"] == selected_state]
            final_df = final_df[final_df["State"] == selected_state]
            
        # If the user has picked a specific Shark, limit partial_states to that shark
        if selected_shark != "All sharks":
            partial_for_map = partial_for_map[partial_for_map["Shark.common.name"] == selected_shark]
            partial_states = partial_states[partial_states["Shark.common.name"] == selected_shark]
            final_histo = final_histo[final_histo["Shark.common.name"] == selected_shark]
            final_df = final_df[final_df["Shark.common.name"] == selected_shark]

        # Histogram update
        histogram_figure = time_hist.update(final_histo, year_range)

        if map_selected_data and "points" in map_selected_data and len(map_selected_data["points"]) > 0:
            selected_uins = [pt["customdata"][0] for pt in map_selected_data["points"]]
            partial_states = partial_states[partial_states["UIN"].isin(selected_uins)]
            partial_sharks = partial_sharks[partial_sharks["UIN"].isin(selected_uins)]
            final_df = final_df[final_df["UIN"].isin(selected_uins)]
        
        # States dropdown options update
        state_options = options(partial_states, "State", "states")
                
        # Sharks dropdown options update
        shark_options = options(partial_sharks, "Shark.common.name", "sharks")
        
        # Update the map
        map_figure = scatter_map_aus.update(partial_for_map, map_selected_data)
        
        # Radar plot: if user brushed points, we might have multiple sharks selected
        radar_figure = plot_radar(map_selected_data, final_df)

        # Heatmap update
        heatmap_figure = heatmap.update(x_heat, y_heat, final_df)
        
        # Barchart update
        barchart_figure = barchart.update(x_bar, y_bar, final_df)

        return map_figure, heatmap_figure, barchart_figure, radar_figure, histogram_figure, state_options, shark_options
    
    
    def options(partial, selected, lselecteds):
        # States dropdown options update
        if partial.empty:
            options = [{"label": f"All {lselecteds} (0)", "value": f"All {lselecteds}"}]
        else:
            options = [
                {
                    "label": f"All {lselecteds} ({len(partial)})",
                    "value": f"All {lselecteds}",
                }
            ]
            # Count instances
            counts = (
                partial.dropna(subset=[selected])
                .groupby(selected)[selected].count()
                .sort_values(ascending=False)
            )
            for item, count in counts.items():
                options.append({"label": f"{item} ({count})", "value": item})
        return options
    
    
    def plot_radar(map_selected_data, final_df):
        # Radar plot: if user brushed points, we might have multiple sharks selected
        if map_selected_data and "points" in map_selected_data and len(map_selected_data["points"]) > 0:
            selected_shark_types = {pt["customdata"][1] for pt in map_selected_data["points"]}
            radar_figure = radar_plot.update_multiple(list(selected_shark_types), final_df)
        else:
            radar_figure = go.Figure()
            axis_labels = [
                "% Injured or Fatal",
                "% Fatal",
                "% Provoked",
                "Avg Length (Norm)",
                "% Victim Below 18"
            ]
            # 5 axis to appear
            radar_figure.add_trace(
                go.Scatterpolar(
                    r=[0, 0, 0, 0, 0],
                    theta=axis_labels,
                    fill='toself',
                    name="No Data",
                    hoverinfo='none'
                )
            )
    
            # Default range 0-100
            radar_figure.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 100]
                    )
                ),
                showlegend=False,
                template="plotly_white",
            )
        return radar_figure

    
    app.run_server(debug=True, dev_tools_ui=False)
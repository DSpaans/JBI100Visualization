from dash import dcc, html
from jbi100_app.views.visualizations.histogram import Histogram
import plotly.graph_objects as go

# Color Palette
BACKGROUND_COLOR = "#F7F7F7"  # Light gray background for the entire layout
CARD_BACKGROUND_COLOR = "#FFFFFF"  # White background for cards
TEXT_COLOR = "#333333"  # Dark text for readability
ACCENT_COLOR = "#007BFF"  # Blue accent color for labels and highlights
HIGHLIGHT_COLOR = "#FF5733"  # Accent color for important elements
SHADOW_COLOR = "rgba(0,0,0,0.1)"  # Light shadow effect for depth

def generate_description_card():
    # A Div containing dashboard title & descriptions.
    
    return html.Div(
        id="description-card",
        children=[
            # sharkify logo
            html.Img(
                src="/assets/sharkify.png",
                style={
                    "width": "100%",
                    "height": "auto",
                    "display": "block",
                    "margin": "0 auto",
                }
            ),
        ],
        style={
            "backgroundColor": CARD_BACKGROUND_COLOR, 
            "borderRadius": "10px", 
            "padding": "10px", 
            "margin": "10px", 
            "boxShadow": f"0 4px 8px {SHADOW_COLOR}"
        }
    )

def clean_column_name(name):
    # Replace underscores and dots with spaces
    name = name.replace('.', ' ').replace('_', ' ')
    # Capitalize each word for a more readable format
    return ' '.join(word.capitalize() for word in name.split())

def generate_control_card(df, column_options_heatmap, column_options_barchart, range_hist):
    # A Div containing controls for graphs.

    return html.Div(
        id="control-card",
        children=[
            # time slider
            html.Div([
                html.Label("Select time range", style={"fontWeight": "bold", "fontSize": "16px", "color": TEXT_COLOR}),
                range_hist,
                make_time_slider(df)
            ], style={"marginBottom": "20px"}),

            html.Hr(style={"borderTop": "1px solid #ccc", "margin": "10px 0"}),

            # month dropdown
            html.Div([
                html.Label("Select month", style={"fontWeight": "bold", "fontSize": "16px", "color": TEXT_COLOR}),
                dcc.Dropdown(
                    id="select-month",
                    options=["All year"],
                    value="All year",
                    clearable=False,
                ),
            ], style={"marginBottom": "5px"}),

            # state dropdown
            html.Div([
                html.Label("Select state", style={"fontWeight": "bold", "fontSize": "16px", "color": TEXT_COLOR}),
                dcc.Dropdown(
                    id="select-state",
                    options=["All states"],
                    value="All states",
                    clearable=False,
                ),
            ], style={"marginBottom": "5px"}),

            # shark dropdown
            html.Div([
                html.Label("Select shark", style={"fontWeight": "bold", "fontSize": "16px", "color": TEXT_COLOR}),
                dcc.Dropdown(
                    id="select-shark",
                    options=["All sharks"],
                    value="All sharks",
                    clearable=False,
                ),
            ], style={"marginBottom": "20px"}),

            html.Hr(style={"borderTop": "1px solid #ccc", "margin": "10px 0"}),

            # select x-axis heatmap
            html.Div([
                html.Label("Select x-axis heatmap", style={"fontWeight": "bold", "fontSize": "16px", "color": TEXT_COLOR}),
                dcc.Dropdown(
                    id="select-x-heatmap",
                    options=[{"label": clean_column_name(col), "value": col} for col in column_options_heatmap],
                    value="Injury.category",
                    style={"width": "100%", "fontSize": "14px", "borderRadius": "5px", "borderColor": "#ccc"}
                ),
            ], style={"marginBottom": "5px"}),

            # select y-axis heatmap
            html.Div([
                html.Label("Select y-axis heatmap", style={"fontWeight": "bold", "fontSize": "16px", "color": TEXT_COLOR}),
                dcc.Dropdown(
                    id="select-y-heatmap",
                    options=[{"label": clean_column_name(col), "value": col} for col in column_options_heatmap],
                    value="Shark.common.name",
                    style={"width": "100%", "fontSize": "14px", "borderRadius": "5px", "borderColor": "#ccc"}
                ),
            ], style={"marginBottom": "20px"}),

            html.Hr(style={"borderTop": "1px solid #ccc", "margin": "10px 0"}),

            # select x-axis barchart
            html.Div([
                html.Label("Select x-axis barchart", style={"fontWeight": "bold", "fontSize": "16px", "color": TEXT_COLOR}),
                dcc.Dropdown(
                    id="select-x-bar",
                    options=[{"label": clean_column_name(col), "value": col} for col in column_options_barchart],
                    value="Injury.category",
                    style={"width": "100%", "fontSize": "14px", "borderRadius": "5px", "borderColor": "#ccc"}
                ),
            ], style={"marginBottom": "5px"}),

            # select y-axis barchart
            html.Div([
                html.Label("Select y-axis barchart", style={"fontWeight": "bold", "fontSize": "16px", "color": TEXT_COLOR}),
                dcc.Dropdown(
                    id="select-y-bar",
                    options=[{"label": clean_column_name(col), "value": col} for col in column_options_barchart],
                    value="Number_of_fatal_incidents", 
                    style={"width": "100%", "fontSize": "14px", "borderRadius": "5px", "borderColor": "#ccc"}
                ),
            ], style={"marginBottom": "10px"}),
        ],
        style={
            "backgroundColor": CARD_BACKGROUND_COLOR, 
            "borderRadius": "10px", 
            "padding": "20px", 
            "marginTop": "20px", 
            "boxShadow": f"0 4px 8px {SHADOW_COLOR}",
            "width": "100%", 
            "maxWidth": "400px"
        }
    )

def make_menu_layout(df, column_options_heatmap, column_options_barchart, range_hist):
    return html.Div(
        children=[
            generate_description_card(),
            generate_control_card(df, column_options_heatmap, column_options_barchart, range_hist)
        ],
        style={
            "display": "flex", 
            "flexDirection": "column", 
            "alignItems": "center", 
            "padding": "20px",
            "backgroundColor": BACKGROUND_COLOR
        }
    )

def make_time_slider(df):
    min_year = df["Incident.year"].min()
    max_year = df["Incident.year"].max()
    return html.Div(
        id="time-slider",
        children=[
            dcc.RangeSlider(
                id="year-slider",
                min=min_year,
                max=max_year,
                marks=None,
                value=[min_year, max_year],
                tooltip={"placement": "bottom", "always_visible": True},
                step=1,
            ),
        ],
        style={
            "backgroundColor": CARD_BACKGROUND_COLOR, 
            "borderRadius": "10px", 
            "padding": "10px", 
            "marginTop": "10px", 
            "boxShadow": f"0 4px 8px {SHADOW_COLOR}"
        }
    )
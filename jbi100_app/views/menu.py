from dash import dcc, html

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
            html.H5(
                "Sharkify", 
                style={
                    "color": ACCENT_COLOR, 
                    "textAlign": "center", 
                    "fontWeight": "bold", 
                    "fontSize": "36px"
                }
            ),
            html.Div(
                id="intro",
                children="Equipping coastguards with essential shark attack insights",
                style={
                    "textAlign": "center", 
                    "color": TEXT_COLOR, 
                    "fontSize": "20px", 
                    "marginTop": "10px"
                }
            ),
        ],
        style={
            "backgroundColor": CARD_BACKGROUND_COLOR, 
            "borderRadius": "10px", 
            "padding": "20px", 
            "margin": "20px", 
            "boxShadow": f"0 4px 8px {SHADOW_COLOR}"
        }
    )

def clean_column_name(name):
    # Replace underscores and dots with spaces
    name = name.replace('.', ' ').replace('_', ' ')
    # Capitalize each word for a more readable format
    return ' '.join(word.capitalize() for word in name.split())

def generate_control_card(df, column_options, column_options_heatmap, column_options_barchart):
    # A Div containing controls for graphs.
    shark_names = sorted(df["Shark.common.name"].dropna().unique())

    return html.Div(
        id="control-card",
        children=[
            html.Div([
                html.Label("Select column", style={"fontWeight": "bold", "fontSize": "16px", "color": TEXT_COLOR}),
                dcc.Dropdown(
                    id="select-hover-column",
                    options=[{"label": clean_column_name(col), "value": col} for col in column_options],
                    value="",
                    style={"width": "100%", "padding": "10px", "fontSize": "14px", "borderRadius": "5px", "borderColor": "#ccc"}
                ),
            ], style={"marginBottom": "20px"}),

            html.Div([
                html.Label("Select x-axis heatmap", style={"fontWeight": "bold", "fontSize": "16px", "color": TEXT_COLOR}),
                dcc.Dropdown(
                    id="select-x-heatmap",
                    options=[{"label": clean_column_name(col), "value": col} for col in column_options_heatmap],
                    value="Injury.category",
                    style={"width": "100%", "padding": "10px", "fontSize": "14px", "borderRadius": "5px", "borderColor": "#ccc"}
                ),
            ], style={"marginBottom": "20px"}),

            html.Div([
                html.Label("Select y-axis heatmap", style={"fontWeight": "bold", "fontSize": "16px", "color": TEXT_COLOR}),
                dcc.Dropdown(
                    id="select-y-heatmap",
                    options=[{"label": clean_column_name(col), "value": col} for col in column_options_heatmap],
                    value="Shark.common.name",
                    style={"width": "100%", "padding": "10px", "fontSize": "14px", "borderRadius": "5px", "borderColor": "#ccc"}
                ),
            ], style={"marginBottom": "20px"}),

            html.Div([
                html.Label("Select x-axis barchart", style={"fontWeight": "bold", "fontSize": "16px", "color": TEXT_COLOR}),
                dcc.Dropdown(
                    id="select-x-bar",
                    options=[{"label": clean_column_name(col), "value": col} for col in column_options_barchart],
                    value="Injury.category",
                    style={"width": "100%", "padding": "10px", "fontSize": "14px", "borderRadius": "5px", "borderColor": "#ccc"}
                ),
            ], style={"marginBottom": "20px"}),

            html.Div([
                html.Label("Select y-axis barchart", style={"fontWeight": "bold", "fontSize": "16px", "color": TEXT_COLOR}),
                dcc.Dropdown(
                    id="select-y-bar",
                    options=[{"label": clean_column_name(col), "value": col} for col in column_options_barchart],
                    value="Number_of_fatal_incidents", 
                    style={"width": "100%", "padding": "10px", "fontSize": "14px", "borderRadius": "5px", "borderColor": "#ccc"}
                ),
            ], style={"marginBottom": "20px"}),

            html.Div([
                html.Label("Select Shark Type (Radar)", style={"fontWeight": "bold", "fontSize": "16px", "color": TEXT_COLOR}),
                dcc.Dropdown(
                    id="select-radar-shark-type",
                    options=[{"label": name, "value": name} for name in shark_names],
                    value=shark_names[0] if shark_names else None,
                    style={"width": "100%", "padding": "10px", "fontSize": "14px", "borderRadius": "5px", "borderColor": "#ccc"}
                ),
            ], style={"marginBottom": "20px"})
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

def make_menu_layout(df, column_options, column_options_heatmap, column_options_barchart):
    return html.Div(
        children=[
            generate_description_card(),
            generate_control_card(df, column_options, column_options_heatmap, column_options_barchart)
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
            html.Label("Time period", style={"fontWeight": "bold", "fontSize": "16px", "color": TEXT_COLOR}),
            dcc.RangeSlider(
                id="year-slider",
                min=min_year,
                max=max_year,
                marks=None,
                vertical=True,
                value=[min_year, max_year],
                tooltip={"placement": "left", "always_visible": True},
                step=1,
                verticalHeight=600,
            ),
        ],
        style={
            "backgroundColor": CARD_BACKGROUND_COLOR, 
            "borderRadius": "10px", 
            "padding": "20px", 
            "marginTop": "30px", 
            "boxShadow": f"0 4px 8px {SHADOW_COLOR}"
        }
    )

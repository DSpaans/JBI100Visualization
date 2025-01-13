from dash import dcc, html

def generate_description_card():
    #A Div containing dashboard title & descriptions.
    return html.Div(
        id="description-card",
        children=[
            html.H5("Sharkify"),
            html.Div(
                id="intro",
                children="Add visualizations to your dashboard.",
            ),
        ],
    )

def clean_column_name(name):
    #cleaning option names
    name = name.replace('.', ' ').replace('_', ' ')
    #capitalizing the names
    return ' '.join(word.capitalize() for word in name.split())


def generate_control_card(df, column_options, column_options_heatmap, column_options_barchart):
    #A Div containing controls for graphs.

    #List of all unique shark names for dropdown
    shark_names = sorted(df["Shark.common.name"].dropna().unique())

    return html.Div(
        id="control-card",
        children=[
            html.Label("Select column"),
            dcc.Dropdown(
                id="select-hover-column",
                options=[{"label": clean_column_name(col), "value": col} for col in column_options],
                value="",
            ),
            html.Label("Select x-axis heatmap"),
            dcc.Dropdown(
                id="select-x-heatmap",
                options=[{"label": clean_column_name(col), "value": col} for col in column_options_heatmap],
                value="Injury.category",
            ),
            html.Label("Select y-axis heatmap"),
            dcc.Dropdown(
                id="select-y-heatmap",
                options=[{"label": clean_column_name(col), "value": col} for col in column_options_heatmap],
                value="Shark.common.name",
            ),
            html.Label("Select x-axis barchart"),
            dcc.Dropdown(
                id="select-x-bar",
                options=[{"label": clean_column_name(col), "value": col} for col in column_options_barchart],
                value="Injury.category",
            ),

            html.Label("Select y-axis barchart"),
            dcc.Dropdown(
                id="select-y-bar",
                options=[{"label": clean_column_name(col), "value": col} for col in column_options_barchart],
                value="Number_of_fatal_incidents", 
            ),
            html.Label("Select Shark Type (Radar)"),
            dcc.Dropdown(
                id="select-radar-shark-type",
                options=[{"label": name, "value": name} for name in shark_names],
                value=shark_names[0] if shark_names else None,
            ),
        ], style={"textAlign": "float-left"}
    )


def make_menu_layout(df, column_options, column_options_heatmap, column_options_barchart):
    return [generate_description_card(), generate_control_card(df, column_options, column_options_heatmap, column_options_barchart)]

def make_time_slider(df):
    min_year = df["Incident.year"].min()
    max_year = df["Incident.year"].max()
    return html.Div(
        id="time-slider",
        # style={
        #     "height": "100%",
        #     "display": "flex",
        #     "flexDirection": "column",
        #     "margin": 0,
        #     "padding": 0,
        # },
        children=[
            html.Label("Time period"),
                dcc.RangeSlider(
                    id="year-slider",
                    min=min_year,
                    max=max_year,
                    marks=None,
                    vertical=True,
                    value=[min_year,max_year],
                    tooltip={
                        "placement": "left",
                        "always_visible": True
                        },
                    step=1,
                    verticalHeight=600,
                    
                ),
        ],
    )
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


def generate_control_card(df, column_options, column_options_heatmap, column_options_barchart):
    #A Div containing controls for graphs.

    #List of all unique shark names for dropdown
    shark_names = sorted(df["Shark.common.name"].dropna().unique())
    states = df["State"].dropna().unique().tolist()
    states.append("All states")
    states = sorted(states)


    return html.Div(
        id="control-card",
        children=[
            html.Label("Select state"),
            dcc.Dropdown(
                id="select-state",
                options=[{"label": state, "value": state} for state in states],
                value="All states",
            ),
            html.Label("Select column"),
            dcc.Dropdown(
                id="select-hover-column",
                options=[{"label": col, "value": col} for col in column_options],
                value="",
            ),
            html.Label("Select x-axis heatmap"),
            dcc.Dropdown(
                id="select-x-heatmap",
                options=[{"label": col, "value": col} for col in column_options_heatmap],
                value="Injury.category",
            ),
            html.Label("Select y-axis heatmap"),
            dcc.Dropdown(
                id="select-y-heatmap",
                options=[{"label": col, "value": col} for col in column_options_heatmap],
                value="Shark.common.name",
            ),
            html.Label("Select x-axis barchart"),
            dcc.Dropdown(
                id="select-x-bar",
                options=[{"label": col, "value": col} for col in column_options_barchart],
                value="Injury.category",
            ),

            html.Label("Select y-axis barchart"),
            dcc.Dropdown(
                id="select-y-bar",
                options=[{"label": col, "value": col} for col in column_options_barchart],
                value="Number_of_fatal_incidents", 
            ),
            html.Label("Select shark type radarplot"),
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
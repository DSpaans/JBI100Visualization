from dash import dcc, html

def generate_description_card():
    """
    :return: A Div containing dashboard title & descriptions.
    """
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


def generate_control_card(df, column_options, column_options_heatmap, column_options_barchart, column_options_radar):
    """

    :return: A Div containing controls for graphs.
    """

    return html.Div(
        id="control-card",
        children=[
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
            html.Label("Radar Axis 1"),
            dcc.Dropdown(
                id="select-radar-col1",
                options=[{"label": col, "value": col} for col in column_options_radar],
                value=column_options_radar[0],  # Default value
            ),
            html.Label("Radar Axis 2"),
            dcc.Dropdown(
                id="select-radar-col2",
                options=[{"label": col, "value": col} for col in column_options_radar],
                value=column_options_radar[1],
            ),
            html.Label("Radar Axis 3"),
            dcc.Dropdown(
                id="select-radar-col3",
                options=[{"label": col, "value": col} for col in column_options_radar],
                value=column_options_radar[2],
            ),
            html.Label("Radar Axis 4"),
            dcc.Dropdown(
                id="select-radar-col4",
                options=[{"label": col, "value": col} for col in column_options_radar],
                value=column_options_radar[3],
            ),
            html.Label("Radar Axis 5"),
            dcc.Dropdown(
                id="select-radar-col5",
                options=[{"label": col, "value": col} for col in column_options_radar],
                value=column_options_radar[4],
            ),
        ], style={"textAlign": "float-left"}
    )


def make_menu_layout(df, column_options, column_options_heatmap, column_options_barchart, column_options_radar):
    return [generate_description_card(), generate_control_card(df, column_options, column_options_heatmap, column_options_barchart, column_options_radar)]

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
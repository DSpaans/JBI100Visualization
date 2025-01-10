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


def generate_control_card(df, column_options, column_options_heatmap, column_options_barchart):
    """

    :return: A Div containing controls for graphs.
    """

    min_year = df["Incident.year"].min()
    max_year = df["Incident.year"].max()

    return html.Div(
        id="control-card",
        children=[
            html.Label("Time period"),
            dcc.RangeSlider(
                        id="year-slider",
                        min=min_year,
                        max=max_year,
                        marks=None,
                        value=[min_year,max_year],
                        tooltip={"placement": "bottom",
                                 "always_visible": True
                                 },
                        step=1
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
        ], style={"textAlign": "float-left"}
    )


def make_menu_layout(df, column_options, column_options_heatmap, column_options_barchart):
    return [generate_description_card(), generate_control_card(df, column_options, column_options_heatmap, column_options_barchart)]

def make_dashboard_layout(visualizations):
    """Creates a modular dashboard layout."""
    layout = []
    for viz in visualizations:
        layout.append(viz)

    return html.Div(layout)
from dash import dcc, html
from ..config import color_list1, color_list2


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


def generate_control_card(df):
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
            html.Label("Color scatterplot 1"),
            dcc.Dropdown(
                id="select-color-scatter-1",
                options=[{"label": i, "value": i} for i in color_list1],
                value=color_list1[0],
            ),
            html.Br(),
            html.Label("Color scatterplot 2"),
            dcc.Dropdown(
                id="select-color-scatter-2",
                options=[{"label": i, "value": i} for i in color_list2],
                value=color_list2[0],
            ),
            # html.Br(),
            # html.Label("Add visualization"),
            # dcc.Button("Add", id="add-visualization", n_clicks=0),
        ], style={"textAlign": "float-left"}
    )


def make_menu_layout(df):
    return [generate_description_card(), generate_control_card(df)]

def make_dashboard_layout(visualizations):
    """Creates a modular dashboard layout."""
    layout = []
    for viz in visualizations:
        layout.append(viz)

    return html.Div(layout)

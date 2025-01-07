from jbi100_app.main import app
from jbi100_app.data import get_data
from jbi100_app.views.menu import make_menu_layout
from jbi100_app.views.visualizations.map import ScatterGeo
from jbi100_app.views.visualizations.scatterplot import Scatterplot
from jbi100_app.views.visualizations.heatmap import Heatmap
from jbi100_app.config import column_options_1
from dash import html, dcc, Dash
from dash.dependencies import Input, Output
import dash

app = Dash(__name__, use_pages=True)

app.layout = html.Div(
    children=[
        dcc.Location(id="url"),  # Tracks the URL
        html.Div(
            children=[
                html.H1("Sharkify Dashboard", style={"textAlign": "center"}),
                html.Div(
                    children=dash.page_container,  # Renders the active page
                    style={"margin-top": "20px"}
                )
            ]
        )
    ]
)

if __name__ == '__main__':
    
    
    app.run_server(debug=True, dev_tools_ui=False)
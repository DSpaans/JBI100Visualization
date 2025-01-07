#Home page
from dash import html, dcc, register_page

register_page(__name__, path="/")

layout = html.Div(
    children=[
        html.H1("Welcome to Sharkify!"),
        html.P("This is the home page of our dashboard."),
    
    
    html.Div(
        children=[
            dcc.Link(
                html.Button("Go to Dashboard"),
                href="/dashboard",
            )
        ]
    )
    
    ],
)
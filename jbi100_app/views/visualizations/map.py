from dash import dcc, html
import plotly.graph_objects as go

class ScatterGeo(html.Div):
    def __init__(self, name, df, feature_x):
        self.html_id = name.lower().replace(" ", "-")
        self.df = df
        self.feature_x = feature_x

        # Equivalent to `html.Div([...])`
        super().__init__(
            className="graph_card",
            style={"justifyContent": "center", "height": "100%"},
            children=[
                html.H6(name),
                dcc.Graph(
                    id=self.html_id,
                    figure=self.update(),  # initial figure (unfiltered)
                    style={'height': '45vh', 'width': '100%'},
                    config={'displayModeBar': True, 'scrollZoom': True}
                )
            ],
        )

    #Update the map with original dataset or the filtered dataset
    def update(self, filtered_df=None, hover_column=""):
        #If there is no filtered_df, default to self.df
        if filtered_df is None:
            filtered_df = self.df
            
        #hover_text = filtered_df['Location'] + "<br>" + Indicent year + ": " + filtered_df[Incident.year].astype(str) + "<br>" + Provoked + ": " + filtered_df[Provoked/unprovoked].astype(str)
        hover_text = (
            filtered_df['Location'].fillna("Unknown") + 
            "<br>" + 
            "Incident Year: " + 
            filtered_df['Incident.year'].fillna("Unknown").astype(str) +
            "<br>" + 
            "Provoked: " + 
            filtered_df['Provoked/unprovoked'].fillna("Unknown").astype(str)
            )

        #Build the figure
        fig = go.Figure(
    data=[
        go.Scattergeo(
            lon=filtered_df['Longitude'],
            lat=filtered_df['Latitude'],
            text=hover_text,
            mode='markers',
            customdata=filtered_df["Shark.common.name"],
            marker=dict(
                color='blue',
                opacity=0.7,
                size=8
            )
        )
    ]
)

        fig.update_layout(
            title = '',
            geo=dict(
                scope='world', 
                center=dict(lat=-28, lon=133), # roughly central Australia
                projection_scale=2.5,         # controls zoom level
                showland=True,
                landcolor='rgb(217, 217, 217)',
                ),
                margin=dict(l=10, r=10, t=40, b=10),
                dragmode='select', #Brushing / Enable selection
                clickmode='event+select' #Clicks can select a single point
        )

        # Highlight selected / unselected traces
        fig.update_traces(
            selected=dict(marker=dict(color='red', size=10)),
            unselected=dict(marker=dict(color='blue', opacity=0.5))
        )
        
        return fig
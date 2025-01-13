from dash import dcc, html
import plotly.graph_objects as go

#lolz
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
                dcc.Graph(id=self.html_id, figure=self.update(),
                style={'height': '45vh', 'width': '100%'}
                )
            ],
        )

    #Update the map with original dataset or the filtered dataset
    def update(self, filtered_df=None, hover_column=""):
        #If there is no filtered_df, default to self.df
        if filtered_df is None:
            filtered_df = self.df
            
        if hover_column not in filtered_df.columns:
            hover_text = filtered_df['Location']
        else:
            #hover_text = filtered_df['Location'] + "<br>" + hover_column + ": " + filtered_df[hover_column].astype(str)
            hover_text = (
                filtered_df['Location'].fillna("Unknown") + 
                "<br>" + 
                hover_column + ": " + 
                filtered_df[hover_column].fillna("Unknown").astype(str)
            )

        #Build the figure
        fig = go.Figure(data=go.Scattergeo(
            lon = filtered_df['Longitude'],
            lat = filtered_df['Latitude'],
            text = hover_text,
            mode = 'markers',
            marker=dict(
                    color='blue',   # Change marker color as needed
                    opacity=0.7,    # I lowered opacity to see overlapping points
                    size=8)
            )
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
                margin=dict(l=10, r=10, t=40, b=10)
        )
        
        return fig
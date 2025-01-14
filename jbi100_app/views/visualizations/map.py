from dash import dcc, html
import plotly.graph_objects as go

class ScatterGeo(html.Div):
    def __init__(self, name, df):
        self.html_id = name.lower().replace(" ", "-")
        self.df = df

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
    def update(self, filtered_df=None, selected_data=None):
        #If there is no filtered_df, default to self.df
        if filtered_df is None:
            filtered_df = self.df

        filtered_df = filtered_df.reset_index(drop=True)
            
        hover_text = (
            "Year: " + filtered_df['Incident.year'].fillna("Unknown").astype(str) + 
            "<br>" + 
            "Location: " + filtered_df['Location'].fillna("Unknown") + 
            "<br>" + 
            "Site: " + filtered_df['Site.category'].fillna("Unknown") + 
            "<br>" + 
            "Shark: " + filtered_df['Shark.common.name'].fillna("Unknown") + 
            "<br>" + 
            "Activity: " + filtered_df['Victim.activity'].fillna("Unknown") + 
            "<br>"+ 
            "Injury: " + filtered_df['Injury.category'].fillna("Unknown") + 
            "<br>"+ 
            filtered_df['Provoked/unprovoked'].fillna("Unknown")
        )

        #Build the figure
        fig = go.Figure(
            data=[
                go.Scattergeo(
                    lon=filtered_df['Longitude'],
                    lat=filtered_df['Latitude'],
                    text=hover_text,
                    mode='markers',
                    customdata= filtered_df[['UIN', 'Shark.common.name']].values,
                    marker=dict(
                        color='blue',
                        opacity=1,
                        size=8
                    )
                )
            ]
        )

        fig.update_layout(
            title = '',
            geo=dict(
                scope='world', 
                center=dict(lat=-25, lon=155), # roughly central Australia
                projection_scale=2.5,         # controls zoom level
                showland=True,
                landcolor='rgb(217, 217, 217)',
                ),
                margin=dict(l=10, r=10, t=40, b=10),
                dragmode='select', #Brushing / Enable selection
        )

        # highlight points with selection other graph
        if selected_data is None:
            selected_index = self.df.index  # show all
        else:
            # Get the selected UINs from selected_data
            selected_uins = [pt["customdata"][0] for pt in selected_data["points"]]
            # Find corresponding indices in the filtered DataFrame based on UIN
            selected_index = filtered_df[filtered_df['UIN'].isin(selected_uins)].index

        # Highlight selected / unselected traces
        fig.update_traces(
            selectedpoints=selected_index,
            selected=dict(marker=dict(color='blue', size=8)),
            unselected=dict(marker=dict(color="rgb(200,200,200)", size=8))
        )
        
        return fig
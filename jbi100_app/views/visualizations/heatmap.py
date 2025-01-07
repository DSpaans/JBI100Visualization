from dash import dcc, html
import plotly.graph_objects as go
import pandas as pd

class Heatmap(html.Div):
    def __init__(self, name, df):
        self.html_id = name.lower().replace(" ", "-")
        self.df = df

        # Available options for the dropdown menus
        self.columns = df.columns.tolist()
        self.default_x = 'Injury.category'
        self.default_y = 'Shark.common.name'

        # Equivalent to `html.Div([...])`
        super().__init__(
            className="graph_card",
            children=[
                html.H6(name),
                dcc.Graph(id=self.html_id, figure=self.update())
            ],
        )


    def _prepare_heatmap_data(df):
        # Group by Injury Category and count occurrences
        grouped_data = df.groupby(['Injury.category', 'Shark.common.name']).size().reset_index(name='Count')
        return grouped_data

    def update(self, filtered_df=None):
        # Generate the one-dimensional heatmap figure
        if filtered_df is None:
            filtered_df = self.df

        # Prepare data for one-dimensional heatmap
        grouped_data = filtered_df.groupby(['Injury.category', 'Shark.common.name']).size().reset_index(name='Count')

        self.fig = go.Figure(
            data=go.Heatmap(
                z=grouped_data['Count'],  # Values for heat intensity
                x=grouped_data['Injury.category'],  # Categories along the x-axis
                y=grouped_data['Shark.common.name'],  # Categories along the y-axis
                colorscale='Reds',
                showscale=True
            )
        )

        # Update layout
        self.fig.update_layout(
            xaxis_title='Injury Category',
            yaxis_title='Shark Common Name',
            # yaxis_showticklabels=False,  # Hide y-axis labels to make it 1D
            margin=dict(l=60, r=20, t=40, b=40)
        )

        return self.fig



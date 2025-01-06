from dash import dcc, html
import plotly.graph_objects as go
import pandas as pd

class Heatmap(html.Div):
    def __init__(self, name, df):
        self.html_id = name.lower().replace(" ", "-")
        self.df = df

        # Prepare data for one-dimensional heatmap
        self.heatmap_data = self._prepare_heatmap_data()
        self.fig = self.update()

        # Equivalent to `html.Div([...])`
        super().__init__(
            className="graph_card",
            children=[
                html.H6(name),
                dcc.Graph(id=self.html_id, figure=self.fig)
            ],
        )


    def _prepare_heatmap_data(self):
        # Group by Injury Category and count occurrences
        grouped_data = self.df.groupby('Injury.Category').size().reset_index(name='Count')
        return grouped_data

    def update(self):
        # Generate the one-dimensional heatmap figure
        self.fig = go.Figure(
            data=go.Heatmap(
                z=[self.heatmap_data['Count']],  # Values for heat intensity
                x=self.heatmap_data['Injury.Category'],  # Categories along the x-axis
                colorscale='Reds',
                showscale=True
            )
        )

        # Update layout
        self.fig.update_layout(
            xaxis_title='Injury Category',
            yaxis_title='',
            yaxis_showticklabels=False,  # Hide y-axis labels to make it 1D
            margin=dict(l=60, r=20, t=40, b=40)
        )

        return self.fig



from dash import dcc, html
import plotly.graph_objects as go
import pandas as pd

class Heatmap(html.Div):
    def __init__(self, name, df):
        self.html_id = name.lower().replace(" ", "-")
        self.df = df

        # Equivalent to `html.Div([...])`
        super().__init__(
            className="graph_card",
            children=[
                html.H6(name),
                dcc.Graph(id=self.html_id)
            ],
        )

    def update(self, selected_x, selected_y, filtered_df=None, selected_data=None):
        # Generate the one-dimensional heatmap figure
        if filtered_df is None:
            filtered_df = self.df

        """        if selected_data and "points" in selected_data and len(selected_data["points"]) > 0:
            selected_ids = {pt["pointIndex"] for pt in selected_data["points"]}
            filtered_df = filtered_df.iloc[list(selected_ids)]
        """
        # Prepare data for one-dimensional heatmap
        grouped_data = filtered_df.groupby([selected_x, selected_y]).size().reset_index(name='Count')

        self.fig = go.Figure(
            data=go.Heatmap(
                z=grouped_data['Count'],  # Values for heat intensity
                x=grouped_data[selected_x],  # Categories along the x-axis
                y=grouped_data[selected_y],  # Categories along the y-axis
                colorscale='Reds',
                showscale=True
            )
        )

        # Update layout
        self.fig.update_layout(
            xaxis_title=selected_x,
            yaxis_title=selected_y,
            # yaxis_showticklabels=False,  # Hide y-axis labels to make it 1D
            margin=dict(l=60, r=20, t=40, b=40)
        )

        return self.fig



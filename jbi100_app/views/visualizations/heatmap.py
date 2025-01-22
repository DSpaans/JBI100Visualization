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
        # Create a complete grid of x and y combinations
        x_values = grouped_data[selected_x].unique()
        y_values = grouped_data[selected_y].unique()
        complete_grid = pd.MultiIndex.from_product([x_values, y_values], names=[selected_x, selected_y]).to_frame(index=False)

        # Merge the complete grid with the existing data, filling missing combinations with 0
        filled_data = pd.merge(complete_grid, grouped_data, how='left', on=[selected_x, selected_y]).fillna({'Count': 0})
        print(grouped_data)

        self.fig = go.Figure(
            data=go.Heatmap(
                z=filled_data['Count'],  # Values for heat intensity
                x=filled_data[selected_x],  # Categories along the x-axis
                y=filled_data[selected_y],  # Categories along the y-axis
                colorscale='Reds',
                showscale=True,
                hovertemplate=(
                    f"<b>{selected_x}</b>: " "%{x}<br>"
                    f"<b>{selected_y}</b>: " "%{y}<br>"
                    "<b>Count</b>: %{z}<extra></extra>"
                )
            )
        )

        # Update layout
        self.fig.update_layout(
            xaxis_title=selected_x,
            yaxis_title=selected_y,
            margin=dict(l=60, r=20, t=40, b=40)
        )

        return self.fig



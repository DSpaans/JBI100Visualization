from dash import dcc, html
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import itertools

class BarChart(html.Div):
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

    def update(self, selected_x, selected_y, filtered_df=None):
        # Barchart update
        # If y column is numeric, we group the x column items and sum the numeric data. 
        # If y column is not numeric, we do a count of rows for each (x,y) combination, then sum across y to get one bar per category of x
        if filtered_df is None:
            filtered_df = self.df

        if pd.api.types.is_numeric_dtype(filtered_df[selected_y]):
            agg_data = (
                filtered_df
                .groupby(selected_x)[selected_y]
                .sum()  # or .mean(), .count(), etc.
                .reset_index()
            )
            y_label = f"Sum of {selected_y}"
            y_values = agg_data[selected_y].values
        else:
            agg_data = (
                filtered_df
                .groupby([selected_x, selected_y])
                .size()
                .reset_index(name='Count')
            )
            
            agg_data = (
                filtered_df
                .groupby([selected_x, selected_y])
                .size()
                .reset_index(name='Count')
            )

        x_values = agg_data[selected_x].values

        palette_alphabet = px.colors.qualitative.Alphabet  # 26 distinct colors
        color_cycle = itertools.cycle(palette_alphabet)
        bar_colors = [next(color_cycle) for _ in range(len(x_values))]

        # Create Bar chart
        fig = go.Figure(
            data=go.Bar(
                x=x_values,
                y=y_values,
                marker_color=bar_colors
            )
        )

        fig.update_layout(
            xaxis_title=selected_x,
            yaxis_title=y_label,
            margin=dict(l=60, r=20, t=40, b=40),
            template="plotly_white"
        )

        return fig
from dash import dcc, html
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
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
        if filtered_df is None:
            filtered_df = self.df

        # Define fixed colors for injury categories
        injury_colors = {
            'fatal': 'red',
            'injured': 'orange',
            'uninjured': 'green'
        }

        # If selected_y is 'Victim.injury', specify victim injury
        if selected_y == 'Victim.injury':
            valid_injury_categories = ['fatal', 'injured', 'uninjured']
            filtered_df = filtered_df[filtered_df['Victim.injury'].isin(valid_injury_categories)]

            # Aggregate the data for the selected_x and the victim.injury categories
            agg_data = (
                filtered_df
                .groupby([selected_x, 'Victim.injury'])
                .size()
                .reset_index(name='Count')
            )

            y_label = "Injury Status"
            x_values = agg_data[selected_x].values
            y_values = agg_data['Count'].values

            # Map injury categories to predefined colors
            bar_colors = [injury_colors[injury] for injury in agg_data['Victim.injury']]

        else:
            # General case for other numeric or categorical columns
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
                y_label = f"Count of {selected_y}"
                y_values = agg_data['Count'].values

            # For other types, use default color palette
            x_values = agg_data[selected_x].values
            palette_alphabet = px.colors.qualitative.Alphabet  # 26 distinct colors
            color_cycle = itertools.cycle(palette_alphabet)
            bar_colors = [next(color_cycle) for _ in range(len(x_values))]

        # Create the Bar chart
        fig = go.Figure(
            data=go.Bar(
                x=x_values,
                y=y_values,
                marker_color=bar_colors  # Apply color to bars, not y-axis labels
            )
        )

        # Update layout with custom y_label and x/y titles
        fig.update_layout(
            xaxis_title=selected_x,
            yaxis_title=y_label,
            margin=dict(l=60, r=20, t=40, b=40),
            template="plotly_white"
        )

        return fig

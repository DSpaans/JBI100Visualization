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

        #fixed colors for injury categories
        injury_colors = {
            'fatal': 'red',
            'injured': 'orange',
            'uninjured': 'green'
        }

        if selected_y == 'Victim.injury':
            valid_injury_categories = ['fatal', 'injured', 'uninjured']
            filtered_df = filtered_df[filtered_df['Victim.injury'].isin(valid_injury_categories)]

            #get data for the selected_x and victim.injury categories
            agg_data = (
                filtered_df
                .groupby([selected_x, 'Victim.injury'])
                .size()
                .reset_index(name='Count')
            )

            #stacked bar chart
            fig = px.bar(
                agg_data,
                x=selected_x,
                y='Count',
                color='Victim.injury',
                color_discrete_map=injury_colors,
                title=f"Stacked Bar Chart of {selected_x} by Injury Status",
                labels={'Count': 'Number of Incidents', selected_x: selected_x}
            )

        else:
            #general case for other numeric or categorical columns
            if pd.api.types.is_numeric_dtype(filtered_df[selected_y]):
                agg_data = (
                    filtered_df
                    .groupby(selected_x)[selected_y]
                    .sum()  
                    .reset_index()
                )
                fig = px.bar(
                    agg_data,
                    x=selected_x,
                    y=selected_y,
                    title=f"Bar Chart of {selected_y} by {selected_x}",
                    labels={selected_y: f"Sum of {selected_y}", selected_x: selected_x}
                )
            else:
                agg_data = (
                    filtered_df
                    .groupby([selected_x, selected_y])
                    .size()
                    .reset_index(name='Count')
                )
                fig = px.bar(
                    agg_data,
                    x=selected_x,
                    y='Count',
                    color=selected_y,
                    title=f"Stacked Bar Chart of {selected_x} by {selected_y}",
                    labels={'Count': 'Number of Incidents', selected_y: selected_y, selected_x: selected_x}
                )

        #update layout for consistency
        fig.update_layout(
            margin=dict(l=60, r=20, t=40, b=40),
            template="plotly_white",
            legend_title=dict(text="Categories"),
            xaxis_title=selected_x,
            yaxis_title="Count" if selected_y != 'Victim.injury' else "Number of Incidents"
        )

        return fig

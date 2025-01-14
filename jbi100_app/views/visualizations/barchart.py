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

        #create color mapping to store consistent color for each attribute
        self.color_mapping = {}

    def update(self, selected_x, selected_y, filtered_df=None):
        if filtered_df is None:
            filtered_df = self.df

        #define fixed colors for injury categories
        injury_colors = {
            'fatal': 'red',
            'injured': 'orange',
            'uninjured': 'green'
        }
        if selected_y == 'Victim.injury':
            valid_injury_categories = ['fatal', 'injured', 'uninjured']
            filtered_df = filtered_df[filtered_df['Victim.injury'].isin(valid_injury_categories)]

            agg_data = (
                filtered_df
                .groupby([selected_x, 'Victim.injury'])
                .size()
                .reset_index(name='Count')
            )

            y_label = "Injury Status"
            x_values = agg_data[selected_x].values
            y_values = agg_data['Count'].values

            bar_colors = [injury_colors[injury] for injury in agg_data['Victim.injury']]

        else:
            if pd.api.types.is_numeric_dtype(filtered_df[selected_y]):
                agg_data = (
                    filtered_df
                    .groupby(selected_x)[selected_y]
                    .sum()  
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

            #for non-injury types, ensure consistent color mapping for the selected_y categories
            x_values = agg_data[selected_x].values
            unique_categories = agg_data[selected_y].unique()

            #create or update the color mapping for the current selected_y attribute
            if selected_y not in self.color_mapping:
                #create a new color cycle for the selected_y if it's not already mapped
                color_cycle = itertools.cycle(px.colors.qualitative.Alphabet)  # 26 distinct colors
                self.color_mapping[selected_y] = {category: next(color_cycle) for category in unique_categories}

            #consistent color mapping for the selected_y
            bar_colors = [self.color_mapping[selected_y][category] for category in agg_data[selected_y]]

        # Create the Bar chart
        fig = go.Figure(
            data=go.Bar(
                x=x_values,
                y=y_values,
                marker_color=bar_colors  #apply color to bars
            )
        )

        #update layout with custom y_label and x/y titles
        fig.update_layout(
            xaxis_title=selected_x,
            yaxis_title=y_label,
            margin=dict(l=60, r=20, t=40, b=40),
            template="plotly_white"
        )

        return fig

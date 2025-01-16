from dash import dcc, html
import plotly.graph_objects as go

class Histogram(html.Div):
    def __init__(self, name, df, show_title=False):
        self.html_id = "histogram"
        self.df = df

        # Equivalent to `html.Div([...])`
        super().__init__(
            className="graph_card",
            children=[
                html.H6(name),
                dcc.Graph(
                    id=self.html_id,
                    config={
                        "displayModeBar": False,
                        "staticPlot": True
                        },
                    style={"height": "180px"},
                    )
            ],
        )

    def update(self, filtered_df, selected_range):
        df = self.df["Incident.year"].dropna()
        df_years = filtered_df["Incident.year"].dropna()
        
        fig = go.Figure(
            data=[
                go.Histogram(
                    x=df_years,
                    marker_color="blue",
                    nbinsx=int(df_years.max() - df_years.min()) + 1,
                )
            ]
        )
        
        fig.add_shape(
            type="rect",
            xref="x",
            yref="paper",
            x0=selected_range[0],
            x1=selected_range[1],
            y0=0,
            y1=1,  # from the bottom to the top of the plot
            fillcolor="LightSkyBlue",
            opacity=0.3,
            layer="below",
            line_width=0
        )
        
        fig.update_xaxes(range=[df.min(), df.max()])

        # Update layout
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(showgrid=False, zeroline=False),
            yaxis=dict(showgrid=False, zeroline=False),
            margin = dict(t=10, l=5, r=5, b=0),
            
        )

        return fig
from dash import dcc, html
import plotly.graph_objects as go
import pandas as pd
import numpy as np

class RadarPlot(html.Div):
    def __init__(self, name, df):
        self.html_id = name.lower().replace(" ", "-")
        self.df = df

        super().__init__(
            className="graph_card",
            children=[
                html.H6(name),
                dcc.Graph(id=self.html_id),
            ],
        )

    def update(self, selected_shark_type, filtered_df=None):

        if filtered_df is None:
            filtered_df = self.df

        #Filter by chosen shark type
        df_shark = filtered_df[filtered_df["Shark.common.name"] == selected_shark_type]

        # If no rows for that shark, then set metrics = 0
        if df_shark.empty:
            pct_injured_or_fatal = 0
            pct_fatal = 0
            pct_provoked = 0
            avg_length = 0
            avg_depth = 0
        else:
            # Total rows for that shark
            total_count = len(df_shark)

            injury_series = df_shark["Victim.injury"].astype(str).str.lower()

            # (1) % of attacks that were "injured" OR "fatal" (EXACT match, no partial matches)
            cond_injured_or_fatal = injury_series.isin(["injured", "fatal"])
            count_injured_or_fatal = cond_injured_or_fatal.sum()
            pct_injured_or_fatal = 100.0 * count_injured_or_fatal / len(df_shark)

            # (2) % of attacks that were "fatal" only
            cond_fatal = injury_series.eq("fatal")  # exact match
            count_fatal = cond_fatal.sum()
            pct_fatal = 100.0 * count_fatal / len(df_shark)

            # (3) % of attacks that were "provoked"
            # "Provoked/unprovoked" = "provoked" or "unprovoked"
            cond_provoked = df_shark["Provoked/unprovoked"].astype(str).str.lower().eq("provoked")
            count_provoked = cond_provoked.sum()
            pct_provoked = 100.0 * count_provoked / total_count

            # (4) average shark length
            # Convert to numeric, ignore invalid entries
            length_series = pd.to_numeric(df_shark["Shark.length.m"], errors="coerce")
            avg_length = length_series.mean(skipna=True)
            if pd.isna(avg_length):
                avg_length = 0

            # (5) average depth
            depth_series = pd.to_numeric(df_shark["Depth.of.incident.m"], errors="coerce")
            avg_depth = depth_series.mean(skipna=True)
            if pd.isna(avg_depth):
                avg_depth = 0

        # Prepare the data for radar
        metrics = [
            pct_injured_or_fatal,
            pct_fatal,
            pct_provoked,
            avg_length,
            avg_depth
        ]
        axis_labels = [
            "% Injured or Fatal",
            "% Fatal",
            "% Provoked",
            "Avg Length (m)",
            "Avg Depth (m)"
        ]

        #Single scatterpolar trace
        fig = go.Figure()

        fig.add_trace(
            go.Scatterpolar(
                r=metrics,
                theta=axis_labels,
                fill='toself',
                name=selected_shark_type,
                hovertemplate='%{theta}: %{r:.2f}<extra></extra>'
            )
        )

        # Pick a radial axis from 0 to 120% of the max (so its sufficiently large)
        max_val = max(metrics) if metrics else 0
        radial_range = [0, max_val * 1.2] if max_val > 0 else [0, 1]

        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=radial_range
                )
            ),
            showlegend=True,
            margin=dict(l=60, r=60, t=40, b=40),
            template="plotly_white",
            title_text=f"Radar for {selected_shark_type}"
        )

        return fig



from dash import dcc, html
import plotly.graph_objects as go
import pandas as pd

class RadarPlot(html.Div):
    def __init__(self, name, df, global_min_length, global_max_length, global_min_depth, global_max_depth):
        self.html_id = name.lower().replace(" ", "-")
        self.df = df

        self.global_min_length = global_min_length
        self.global_max_length = global_max_length
        self.global_min_depth = global_min_depth
        self.global_max_depth = global_max_depth

        super().__init__(
            className="graph_card",
            children=[
                html.H6(name),
                dcc.Graph(id=self.html_id),
            ],
        )

    def normalize_to_100(self, value, min_val, max_val):
        #To convert value to a 0-100 scale
        if pd.isna(value):
            return 0
        if max_val == min_val:
            return 0
        return 100 * (value - min_val) / (max_val - min_val)
    
    def compute_metrics(self, df_shark):
        #Given a DataFrame 'df_shark' for a single shark type, compute the 5 metrics:
        #  1) % Injured or Fatal
        #  2) % Fatal
        #  3) % Provoked
        #  4) Avg Length (normalized)
        #  5) Avg Depth (normalized)
        if df_shark.empty:
            # If no rows, return all zeros
            return 0, 0, 0, 0, 0

        total_count = len(df_shark)
        injury_series = df_shark["Victim.injury"].astype(str).str.lower()

        # (1) % of attacks "injured" or "fatal"
        cond_injured_or_fatal = injury_series.isin(["injured", "fatal"])
        pct_injured_or_fatal = 100.0 * cond_injured_or_fatal.sum() / total_count

        # (2) % of attacks strictly "fatal"
        cond_fatal = injury_series.eq("fatal")
        pct_fatal = 100.0 * cond_fatal.sum() / total_count

        # (3) % Provoked
        prov_series = df_shark["Provoked/unprovoked"].astype(str).str.lower().eq("provoked")
        pct_provoked = 100.0 * prov_series.sum() / total_count

        # (4) Average shark length (normalized 0-100)
        length_series = pd.to_numeric(df_shark["Shark.length.m"], errors="coerce")
        avg_length = length_series.mean(skipna=True) or 0
        avg_length_norm = self.normalize_to_100(
            avg_length, 
            self.global_min_length, 
            self.global_max_length
        )

        # (5) Average depth (normalized 0-100)
        depth_series = pd.to_numeric(df_shark["Depth.of.incident.m"], errors="coerce")
        avg_depth = depth_series.mean(skipna=True) or 0
        avg_depth_norm = self.normalize_to_100(
            avg_depth, 
            self.global_min_depth, 
            self.global_max_depth
        )

        return (
            pct_injured_or_fatal,
            pct_fatal,
            pct_provoked,
            avg_length_norm,
            avg_depth_norm
        )

    def update(self, selected_shark_type, filtered_df=None):

        if filtered_df is None:
            filtered_df = self.df

        #Filter by chosen shark type
        df_shark = filtered_df[filtered_df["Shark.common.name"] == selected_shark_type]

        (pct_injured_or_fatal,
         pct_fatal,
         pct_provoked,
         avg_length_norm,
         avg_depth_norm) = self.compute_metrics(df_shark)

        # Prepare the data for radar
        metrics = [
            pct_injured_or_fatal,
            pct_fatal,
            pct_provoked,
            avg_length_norm,
            avg_depth_norm
        ]
        axis_labels = [
            "% Injured or Fatal",
            "% Fatal",
            "% Provoked",
            "Avg Length (Norm)",
            "Avg Depth (Norm)"
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
        radial_range = [0, max_val * 1] if max_val > 0 else [0, 1]

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
    
    def update_multiple(self, shark_types, filtered_df=None):
        # Multitrace radarplot for multiple shark types
        if filtered_df is None:
            filtered_df = self.df

        axis_labels = [
            "% Injured or Fatal",
            "% Fatal",
            "% Provoked",
            "Avg Length (Norm)",
            "Avg Depth (Norm)"
        ]
        fig = go.Figure()
        all_values = []

        for st in shark_types:
            df_shark = filtered_df[filtered_df["Shark.common.name"] == st]
            (pct_injured_or_fatal,
             pct_fatal,
             pct_provoked,
             avg_length_norm,
             avg_depth_norm) = self.compute_metrics(df_shark)

            # Collect them into a list for this shark
            metrics = [
                pct_injured_or_fatal,
                pct_fatal,
                pct_provoked,
                avg_length_norm,
                avg_depth_norm
            ]
            # Extend all_values so we can find the global max
            all_values.extend(metrics)

            fig.add_trace(
                go.Scatterpolar(
                    r=metrics,
                    theta=axis_labels,
                    fill='toself',
                    name=st,  # legend entry
                    hovertemplate='%{theta}: %{r:.2f}<extra></extra>'
                )
            )

        # Determine global radial range from all traces
        max_val = max(all_values) if all_values else 0
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
            title_text=""
        )

        return fig



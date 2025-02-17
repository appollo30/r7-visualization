from src.plots.base_plot import SinglePlot
import plotly.graph_objects as go
from plotly.subplots import make_subplots

class XYZPlot(SinglePlot):
    def make_plot(self) -> None:
        fig = make_subplots(
            rows=3,
            cols=1,
            shared_xaxes=True,
            subplot_titles=["X", "Y", "Z"],
            x_title="Time (s)",
            y_title="Acceleration (g)"
            )

        for df,name in zip(self.dfs,self.names):
            fig.add_trace(
                go.Scatter(x=df["time (s)"],
                        y=df["X (g)"],
                        mode='lines',
                        name=name,
                        legendgroup=name,
                        line={"color" : self.color_dict[name]}
                        ),
                row=1,
                col=1)
            fig.add_trace(
                go.Scatter(x=df["time (s)"],
                        y=df["Y (g)"],
                        mode='lines',
                        name=name,
                        legendgroup=name,
                        line={"color" : self.color_dict[name]},
                        showlegend=False
                        ),
                row=2, col=1)
            fig.add_trace(
                go.Scatter(
                    x=df["time (s)"],
                    y=df["Z (g)"],
                    mode='lines',
                    name=name,
                    legendgroup=name,
                    line={"color" : self.color_dict[name]},
                    showlegend=False
                    ),
                row=3,
                col=1
                )
        fig.update_layout(hovermode="x unified", title_text="Accélération en X, Y et Z en fonction du temps")
        self.cache_plot = fig
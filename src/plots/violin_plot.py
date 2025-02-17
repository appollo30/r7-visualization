from .base_plot import Plot
import plotly.graph_objects as go

class ViolinPlot(Plot):
    def create_plot(self) -> go.Figure:
        fig = go.Figure()

        for df,name in zip(self.dfs,self.names):
            fig.add_trace(
                go.Violin(
                    y=df["acceleration (g)"],
                    name=name,
                    box_visible=True,
                    meanline_visible=True,
                    line={"color" : self.color_dict[name]}
                    ),
                )
        fig.update_yaxes(title_text="Acceleration (g)")
        fig.update_layout(title_text="Distribution de l'accélération")
        return fig
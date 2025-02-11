import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def multi_line_graph(dfs, names, mode='lines'):
    fig = go.Figure()
    
    for df,name in zip(dfs,names):
        fig.add_trace(go.Scatter(x=df["time (s)"], y=df["acceleration (g)"], mode=mode, name=name))
    fig.update_layout(hovermode="x")
    fig.update_xaxes(title_text="Time (s)")
    fig.update_yaxes(title_text="Acceleration (g)")
    return fig

def violin_plots(dfs, names):
    fig = go.Figure()
    
    for df,name in zip(dfs,names):
        fig.add_trace(go.Violin(y=df["acceleration (g)"], name=name, box_visible=True, meanline_visible=True))
    fig.update_yaxes(title_text="Time (s)")
    return fig

def xyz_plot(dfs, names):
    colors = px.colors.qualitative.Plotly
    color_dict = {name: color for name, color in zip(names, colors)}
    
    fig = make_subplots(
        rows=3,
        cols=1,
        shared_xaxes=True,
        subplot_titles=["X", "Y", "Z"],
        x_title="Time (s)",
        y_title="Acceleration (g)"
        )
    
    for df,name in zip(dfs,names):
        fig.add_trace(
            go.Scatter(x=df["time (s)"],
                       y=df["X (g)"],
                       mode='lines',
                       name=name,
                       legendgroup=name,
                       line={"color" : color_dict[name]}
                       ),
            row=1,
            col=1)
        fig.add_trace(
            go.Scatter(x=df["time (s)"],
                       y=df["Y (g)"],
                       mode='lines',
                       name=name,
                       legendgroup=name,
                       line={"color" : color_dict[name]},
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
                line={"color" : color_dict[name]},
                showlegend=False
                ),
            row=3,
            col=1
            )
    fig.update_layout(hovermode="x")
    return fig

def stacked_plot(dfs, names):
    n = len(names)
    
    colors = px.colors.qualitative.Plotly
    color_dict = {name: color for name, color in zip(names, colors)}
    
    fig = make_subplots(rows=n,
                        cols=2,
                        shared_yaxes=True,
                        horizontal_spacing=0,
                        column_widths=[0.8, 0.2],
                        x_title="Time (s)",
                        y_title="Acceleration (g)",
            )
    
    for i, (df,name) in enumerate(zip(dfs,names)):
        fig.add_trace(
            go.Scatter(
                x=df["time (s)"],
                y=df["acceleration (g)"],
                mode='lines',
                name=name,
                line={"color" : color_dict[name]},
                legendgroup=name
                ),
            row=i+1,
            col=1,
            )
        fig.add_trace(
            go.Violin(
                y=df["acceleration (g)"], 
                name=name, 
                box_visible=True, 
                meanline_visible=True, 
                line={"color" : color_dict[name]},
                legendgroup=name,
                showlegend=False,
                ), 
            row=i+1, 
            col=2)
    fig.update_layout(hovermode="x")
    
    return fig
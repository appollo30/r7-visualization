import plotly.express as px
import plotly.graph_objects as go

def multi_line_graph(dfs, names):
    fig = go.Figure()
    
    for df,name in zip(dfs,names):
        fig.add_trace(go.Scatter(x=df["time (s)"], y=df["acceleration (g)"], mode='lines', name=name))
    return fig

def boxplots(dfs, names):
    fig = go.Figure()
    
    for df,name in zip(dfs,names):
        fig.add_trace(go.Box(y=df["acceleration (g)"], name=name))
    return fig
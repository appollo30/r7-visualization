import numpy as np
import pandas as pd
import streamlit as st
from src.walking_recording import WalkingRecording
from collections import Counter
from typing import List
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import onnxruntime as ort

names = sorted(['Antoine', 'Corentin', 'Felix', 'Leo', 'Vladislav', 'Matthieu', 'Serge'])
color_scheme = {name : color for name, color in zip(names,px.colors.qualitative.Plotly)}

@st.cache_resource
def get_inference_session(model_path : str) -> ort.InferenceSession:
    session = ort.InferenceSession(model_path)
    return session

def create_sequences(data, sequence_size=250, hop_length=1) -> np.ndarray:
    sequences = []
    for start in range(0, len(data) - sequence_size + 1, hop_length):
        sequence = data[start:start + sequence_size]
        if len(sequence) == sequence_size:
            sequences.append(sequence)
    sequences = np.array(sequences)
    return np.reshape(sequences,(sequences.shape[0],sequences.shape[1],1))

def get_counter(predicted_names : List[str]) -> Counter:
    return Counter(predicted_names).most_common()

def predict_from_wr(walking_recording : WalkingRecording, inference_session, verbose : bool = True):
    sequence_size = inference_session.get_inputs()[0].shape[1]
    
    df = walking_recording.df
    data = df["acceleration (g)"].values
    sequences = create_sequences(data, sequence_size) 
    prediction = inference_session.run(None, {inference_session.get_inputs()[0].name: sequences.astype(np.float32)})[0]
    predicted_indices = np.argmax(prediction,axis=1)
    predicted_names = [names[idx] for idx in predicted_indices]
    return predicted_names

def to_gantt(predicted_names):
    output_data = []
    start = 0
    finish = 1
    state = predicted_names[0]
    for i, name in enumerate(predicted_names):
        finish = i
        if name != state:
            output_data.append({'prediction' : state, "start" : start, "finish" : finish})
            start = finish
            state = name
    output_data.append({'prediction' : state, "start" : start, "finish" : finish})
    output_df = pd.DataFrame(output_data)
    return output_df

def show_container(walking_recording : WalkingRecording, predicted_names : List[str]):
    c = get_counter(predicted_names)
    n = len(predicted_names)
    with st.container(border=True,):
        st.caption(f"{walking_recording.name}/{walking_recording.file_name}")
        st.markdown(f"### Utilisateur prédit : **{c[0][0]}**")
        st.plotly_chart(make_area_plot(walking_recording.df, predicted_names), use_container_width=True)
        st.markdown("### Détail des prédictions :")
        for name, count in c:
            st.markdown(f"{name} : {count/n:.2%}")
        

def make_area_plot(df,predicted_names):
    gantt = to_gantt(predicted_names)
    nameset = set()
    fig = go.Figure()
    for i, row in gantt.iterrows():
        start = row["start"]
        finish = row["finish"]
        name = row["prediction"]
        df_subset = df[start:finish+1]
        trace = go.Scatter(
            x = df_subset["time (s)"],
            y = df_subset["acceleration (g)"],
            mode="lines",
            fill='tozeroy',
            line_color = color_scheme[name],
            legendgroup=name,
            name=name,  
        )
        if name in nameset:
            trace.update(showlegend=False)
        else:
            nameset.add(name)
        fig.add_trace(trace)
    
    fig.update_layout(
        title="Prédicitons de l'utilisateur",
        xaxis_title="Time (s)",
        yaxis_title="Acceleration (g)",
        showlegend=True,
        legend_title_text='Prédictions',
    )
    
    return fig

        
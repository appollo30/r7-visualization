import numpy as np
import pandas as pd
import streamlit as st
import keras
from src.walking_recording import WalkingRecording
from collections import Counter
from typing import List

names = ['Antoine', 'Corentin', 'Felix', 'Leo', 'Vladislav', 'Matthieu', 'Serge']

@st.cache_data
def load_model(verbose : bool = True) -> keras.Model :
    if verbose:
        with st.spinner("Chargement du modèle...", show_time=True):
            model = keras.saving.load_model("models/cnn_3layers_75.46_20250324215033/model_250.keras")
    else :
        model = keras.saving.load_model("models/cnn_3layers_75.46_20250324215033/model_250.keras")
    return model

def create_sequences(data, sequence_size=250, hop_length=1) -> np.ndarray:
    sequences = []
    for start in range(0, len(data) - sequence_size + 1, hop_length):
        sequence = data[start:start + sequence_size]
        if len(sequence) == sequence_size:
            sequences.append(sequence)
    sequences = np.array(sequences)
    return np.reshape(sequences,(sequences.shape[0],sequences.shape[1],1))

def get_counter(predicted_names : List[str]) -> Counter:
    return sorted(Counter(predicted_names))

@st.cache_data
def predict_from_wr(walking_recording : WalkingRecording, model : keras.Model, verbose : bool = True):
    sequence_size = model.layers[0].input.shape[1]
    
    df = walking_recording.df
    data = df["acceleration (g)"].values
    sequences = create_sequences(data, sequence_size) 
    prediction = model.predict(sequences)
    predicted_indices = np.argmax(prediction,axis=1)
    predicted_names = [names[idx] for idx in predicted_indices]
    return predicted_names

def get_predictions_plot(walking_recording : WalkingRecording, predicted_names : List[str], sequence_size):
    pass
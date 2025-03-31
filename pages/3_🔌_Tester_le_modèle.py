from src.file_uploader import handle_file_uploader
from src.walking_recording import WalkingRecording
from src.plot_factory import PlotFactory
import pandas as pd
import streamlit as st
import keras

@st.cache_data
def get_model():
    model = keras.saving.load_model("models/cnn_3layers_75.46_20250324215033/model_250.keras")

def main():
    st.title("Tester le modèle")
    
    walking_recordings = handle_file_uploader()
    
    markdown_text = "**Fichiers ajoutés**"
    for recording in walking_recordings:
        markdown_text += f"\n- {recording.name}/{recording.file_name}"
    st.markdown(markdown_text)
    

main()
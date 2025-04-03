from src.file_uploader import handle_file_uploader
from src.walking_recording import WalkingRecording
from src.plot_factory import PlotFactory
from src.ml_utils import load_model, predict_from_wr
import pandas as pd
import streamlit as st
import keras

def main():
    st.title("Tester le modèle")
    
    walking_recordings = handle_file_uploader()
    
    model = load_model()
    
    if len(walking_recordings) > 0:
        with st.spinner("Prédiction en cours"):
            prediction = predict_from_wr(walking_recordings[0],model)
            
        st.write(prediction)
    

main()
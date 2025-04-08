from src.file_uploader import handle_file_uploader
from src.walking_recording import WalkingRecording
from src.plot_factory import PlotFactory
from src.ml_utils import predict_from_wr, show_container, get_inference_session
import streamlit as st

def main():
    st.set_page_config(
        page_title="Tester le modèle",
        layout="wide",
    )
    
    st.title("Tester le modèle")
    
    inference_session = get_inference_session("models/cnn_3layers_79.30_20250408092059/model_250.onnx")
    
    walking_recordings = handle_file_uploader()
    
    col1, col2 = st.columns(2)
    
    for i, wr in enumerate(walking_recordings):
        predicted_names = predict_from_wr(wr, inference_session)
        if i % 2 == 0:
            with col1:
                show_container(wr, predicted_names)
        else:
            with col2:
                show_container(wr, predicted_names)
        
    

main()
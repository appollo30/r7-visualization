from src.file_uploader import handle_file_uploader
from src.ml_utils import predict_from_wr, show_container, get_inference_session
import streamlit as st

def main():
    st.set_page_config(
        page_title="Tester le modèle",
        layout="wide",
    )
    
    inference_session = get_inference_session("models/cnn_3layers_84.03_20250409003023/model_250.onnx")
    
    st.title("Tester le modèle")
    
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
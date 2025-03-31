from typing import List
from src.walking_recording import WalkingRecording
from src.data_processing_utils import raw_schema, processed_schema, process
import streamlit as st
import pandas as pd
import pandera as pa

def handle_file_uploader(verbose=True) -> List[WalkingRecording]:
    expander = st.expander("Ajouter vos propres fichiers")
    
    col1, col2 = expander.columns([0.3, 0.7])
    
    data_type = col1.radio(
        "Quel type de données souhaitez-vous ajouter ?",
        ("Données brutes", "Données traitées"),
        index=1
    )
    is_raw_data = data_type == "Données brutes"
    
    uploaded_files = col2.file_uploader(
        "Choisissez des fichiers CSV",
        type="csv",
        accept_multiple_files=True
    )
    
    walking_recordings = []
    for uploaded_file in uploaded_files:
        try:
            if is_raw_data:
                raw_data = pd.read_csv(uploaded_file, parse_dates=["Timestamp"])
                raw_data = raw_schema.validate(raw_data)
                df = process(raw_data)
            else:
                df = pd.read_csv(uploaded_file)
                df = processed_schema.validate(df)
        except (pd.errors.ParserError, pa.errors.SchemaError, ValueError) as e:
            st.error(f"Le fichier {uploaded_file.name} n'est pas valide : {e}")
            return []
        walking_recording = WalkingRecording(df, name="Custom",file_name=f"{uploaded_file.name}")
        walking_recordings.append(walking_recording)
    
    if verbose and len(walking_recordings) > 0:
        markdown_text = "**Fichiers ajoutés**"
        for recording in walking_recordings:
            markdown_text += f"\n- {recording.name}/{recording.file_name}"
        expander.markdown(markdown_text)
    
    return walking_recordings

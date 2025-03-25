from src.file_uploader import handle_file_uploader
from src.walking_recording import WalkingRecording
from src.plot_factory import PlotFactory
import streamlit as st

def main():
    walking_recordings = handle_file_uploader()
    
    markdown_text = "**Fichiers ajoutés**"
    for recording in walking_recordings:
        markdown_text += f"\n- {recording.name}/{recording.file_name}"
    st.markdown(markdown_text)

main()
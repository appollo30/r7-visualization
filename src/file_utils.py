import random
from typing import List
import glob
import os
import streamlit as st
from src.walking_recording import WalkingRecording
from src.data_processing_utils import processed_schema

@st.cache_data
def get_all_file_names() -> List[str]:
    random.seed(42)
    all_files = glob.glob("data/processed/*/*")
    all_files_no_prefix = [os.path.relpath(f, "data/processed") for f in all_files]
    random.shuffle(all_files_no_prefix)
    return all_files_no_prefix

@st.cache_data
def get_specific_file(name: str) -> WalkingRecording:
    file_name = f"data/processed/{name}"
    walking_recording = WalkingRecording.from_csv(file_name)
    return walking_recording
import random
from typing import List
import glob
import os
import streamlit as st

@st.cache_data
def get_all_files() -> List[str]:
    random.seed(42)
    all_files = glob.glob("data/processed/*/*")
    all_files_no_prefix = [os.path.relpath(f, "data/processed") for f in all_files]
    random.shuffle(all_files_no_prefix)
    return all_files_no_prefix

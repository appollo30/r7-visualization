import streamlit as st
import glob
import os

if __name__ == '__main__':
    input_path = glob.glob("./data/output/*")
    # Les noms de chaque membre du groupe, associés aux chemins de leurs fichiers
    members_names = {os.path.basename(elt) : elt for elt in input_path}
    
    st.title("Visualisation des données")
    
    selection = st.pills("Choisissez un membre du groupe",
                         list(members_names.keys()),
                         selection_mode="multi")
    
    
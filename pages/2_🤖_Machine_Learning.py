import pandas as pd
import streamlit as st
import plotly.express as px
from src.file_utils import get_all_file_names, get_specific_file
from src.plots.frequency_plot import FrequencyPlot

@st.cache_data
def get_metrics_df():
    files = get_all_file_names()
    recordings = [get_specific_file(f) for f in files]
    freq_plot = FrequencyPlot(recordings)
    metrics = freq_plot.get_metrics_df(needs_identifier=False)
    return pd.DataFrame(metrics)

def make_scatter(df, x, y):
    colors = px.colors.qualitative.Plotly
    fig = px.scatter(
        df,
        x=x,
        y=y,
        color="Nom",
        hover_data={"Fichier source": True},
        color_discrete_sequence=colors
    )
    fig.update_traces(textposition='top center', marker=dict(size=15))
    fig.update_layout(
        title=f"{x} vs {y}",
        xaxis_title=x,
        yaxis_title=y,
        hovermode="closest",
    )
    return fig

def handle_scatterplots(metrics_df):
    choices = {
        "Fréquence des pas par fft (Hz)",
        "Fréquence des pas par comptage (Hz)",
        "Amplitude de l'accélération (g)",
        "Ecart-type de la durée des pas (s)"
    }
    selection = st.multiselect(
        "Choisissez les features à comparer",
        list(choices),
        default=["Fréquence des pas par comptage (Hz)", "Amplitude de l'accélération (g)"],
        max_selections=2
    )
    if len(selection) == 2:
        st.plotly_chart(make_scatter(metrics_df, selection[0], selection[1]))
    else:
        st.write("### Veuillez sélectionner deux features")

def main():
    st.set_page_config(page_title="Machine Learning", layout="wide")
    st.title("Analyse des données par machine learning")
    metrics_df = get_metrics_df()
    st.markdown("""
                ## Feature Engineering
                
                A partir des données de démarche, nous avons pu extraire manuellement un certain
                nombre de features qui représentent les enregistrements.                
    """)
    st.table(metrics_df.head(5))
    st.markdown("""
                On peut déjà s'intéresser à la distribution de ces features pour voir si elles sont
                discriminantes dans la reconnaissance de la démarche.
    """)
    handle_scatterplots(metrics_df)
    st.markdown("""
                ## Modélisation
                
                ### Premier modèle : SVM
                
                Pour commencer, nous allons utiliser un modèle de SVM pour classifier les enregistrements
                de démarche. Nous allons utiliser les features extraites précédemment pour entraîner le modèle.
                """)


main()

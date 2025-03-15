import os
import glob
import pandas as pd
import numpy as np

def _norm(df):
    """
    Calculer la norme du vecteur d'accélération
    """
    df["acceleration (g)"] = np.sqrt(df["X (g)"]**2 + df["Y (g)"]**2 + df["Z (g)"]**2)
    return df

def _trim(df):
    """
    Réduire les données pour supprimer la première et la dernière seconde de l'enregistrement
    """
    first_sec = df.iloc[0]["Timestamp"]
    last_sec = df.iloc[-1]["Timestamp"]

    # Garder uniquement les données entre la première et la dernière seconde exclues
    df = df.query("Timestamp > @first_sec & Timestamp < @last_sec")
    df = df.reset_index(drop=True)
    return df

def _set_time(df):
    """
    Définir la colonne de temps pour qu'elle soit comptée en secondes depuis le début
    de l'enregistrement
    """
    df = df.copy()
    df['time (s)'] = 0
    df['time (s)'] = df['time (s)'].astype(float)
    group = df.groupby("Timestamp")

    for idx, (name, group_df) in enumerate(group):
        group_df["time (s)"] = idx + np.linspace(0, 1, len(group_df)+1)[:-1]
        df.update(group_df)

    df["time (s)"] = df["time (s)"].astype(float)
    return df

def _get_timestamp_precision(df):
    """
    Obtenir la précision des timestamps

    Returns:
        str: La précision des timestamps,
        "s" si la précision est en secondes,
        "ms" si la précision est en millisecondes,
        "us" si la précision est en microsecondes
    """
    date = df["Timestamp"][0]
    if date.microsecond == 0:
        return "s"
    elif date.microsecond % 1000 == 0:
        return "ms"
    else:
        return "us"

def _reinterpolate(df):
    """
    Réinterpoler les données pour avoir une fréquence de 100Hz
    """
    df['time (timedelta)'] = pd.to_timedelta(df['time (s)'], unit='s')
    df = df.set_index('time (timedelta)')
    df = df.resample('10ms').mean()
    df = df.interpolate(method='linear')
    df['time (s)'] = df.index.total_seconds()
    return df

def process(df):
    """
    Appliquer les transformations sur le dataframe

    Returns:
        pd.DataFrame: Le dataframe transformé
    """
    df["Timestamp"] = pd.to_datetime(df["Timestamp"])
    df = _norm(df)
    precision = _get_timestamp_precision(df)
    if precision == "s":
        df = _trim(df)
        df = _set_time(df)
    else:
        df['time (s)'] = (df["Timestamp"] - df["Timestamp"].iloc[0]).dt.total_seconds()
    df = df.drop(columns=["Timestamp"])
    cols = df.columns.tolist()
    cols = cols[-1:] + cols[:-1]
    df = df[cols]
    df = _reinterpolate(df)
    return df


if __name__ == "__main__":
    input_path = glob.glob("./data/raw/*")
    # Les noms de chaque membre du groupe, associés aux chemins de leurs fichiers
    members_names = {os.path.basename(elt): elt for elt in input_path}
    for name, path in members_names.items():
        input_files = glob.glob(f"{path}/*")
        print(name)
        for f in input_files:
            df = pd.read_csv(f)
            print(f"Traitement de {f}")
            df = process(df)
            OUTPUT_DIR = f"./data/processed/{name}"
            if not os.path.exists(OUTPUT_DIR):
                os.makedirs(OUTPUT_DIR)
            df.to_csv(f"{OUTPUT_DIR}/{os.path.basename(f)}", index=False)

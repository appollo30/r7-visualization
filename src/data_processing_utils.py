import pandas as pd
import numpy as np
import pandera as pa
from pandera import Column, DataFrameSchema, Check

raw_schema = DataFrameSchema(
    columns={
        "X (g)": Column(float),
        "Y (g)": Column(float),
        "Z (g)": Column(float),
        "Timestamp": Column(
            pa.DateTime,
            checks=[
                # Vérifier que les timestamps sont triés dans l'ordre croissant
                Check(
                    lambda ts: ts.is_monotonic_increasing, element_wise=False,
                    error="Les timestamps doivent être triés dans l'ordre croissant"
                ),
                # Vérifier que la durée entre le premier et le dernier timestamp est < 300 secondes
                Check(
                    lambda ts: (ts.max() - ts.min()).total_seconds() < 300,
                    element_wise=False,
                    error="La durée entre le premier et le dernier timestamp doit être < 300 secondes"
                ),
                # Vérifier que la durée entre le premier et le dernier timestamp est > 3 secondes
                Check(
                    lambda ts: (ts.max() - ts.min()).total_seconds() > 3,
                    element_wise=False,
                    error="La durée entre le premier et le dernier timestamp doit être > 3 secondes"
                ),
                # Vérifier que 2 timestamps consécutifs ne diffèrent pas de plus de 2 secondes
                Check(
                    lambda ts: (ts.diff()[1:].dt.total_seconds() <= 2).all(),
                    element_wise=False,
                    error="Les timestamps ne sont pas espacés de 2 secondes au maximum"
                )
            ]
        )
    },
    ordered=True,
    coerce=True,
    strict=True
)

processed_schema = DataFrameSchema(
    columns={
        "time (s)": Column(
            float,
            checks=[
                Check(lambda x: x >= 0, element_wise=True, error="time (s) doit être >= 0"),
                Check(
                    lambda ts: ts.is_monotonic_increasing, element_wise=False,
                    error="Les timestamps doivent être triés dans l'ordre croissant"
                ),
                Check(
                    lambda ts: (ts.max() - ts.min()) < 300,
                    element_wise=False,
                    error="La durée entre le premier et le dernier timestamp doit être < 300 secondes"
                ),
                Check(
                    lambda ts: (ts.max() - ts.min()) > 3,
                    element_wise=False,
                    error="La durée entre le premier et le dernier timestamp doit être > 3 secondes"
                ),
                Check(
                    lambda ts: np.allclose(np.diff(ts), np.diff(ts)[0]),
                    element_wise=False,
                    error="Les timestamps ne sont pas augmentés par un facteur constant"
                )
            ]
        ),
        "X (g)": Column(float),
        "Y (g)": Column(float),
        "Z (g)": Column(float),
        "acceleration (g)": Column(
            float,
            checks=[
                Check.ge(0),
            ]
        )
    },
    checks=[
        Check(
            lambda df: abs(df["X (g)"]**2 + df["Y (g)"]**2 + df["Z (g)"]**2 - df["acceleration (g)"]**2).max() < 1e-6,
        )
    ],
    ordered=True,
    coerce=True,
    strict=True
)

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

def validate_raw(df) -> bool:
    """
    Valider le dataframe
    """
    try:
        raw_schema.validate(df)
        print("Validation réussie!")
        return True
    except pa.errors.SchemaError as e:
        print(f"Erreur de validation: {e}")
        return False
        
def validate_processed(df):
    """
    Valider le dataframe
    """
    try:
        processed_schema.validate(df)
        print("Validation réussie!")
        return True
    except pa.errors.SchemaError as e:
        print(f"Erreur de validation: {e}")
        return False

def process(df):
    """
    Appliquer les transformations sur le dataframe

    Returns:
        pd.DataFrame: Le dataframe transformé
    """
    df = df.copy()
    precision = _get_timestamp_precision(df)
    if precision == "s":
        df = _trim(df)
        df = _set_time(df)
    else:
        df['time (s)'] = (df["Timestamp"] - df["Timestamp"].iloc[0]).dt.total_seconds()
    df = _norm(df)
    df = df.drop(columns=["Timestamp"])
    cols = df.columns.tolist()
    cols = cols[-1:] + cols[:-1]
    df = df[cols]
    df = _reinterpolate(df)
    return df

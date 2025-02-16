import os
import glob
import pandas as pd
import numpy as np

class DataFormatting:
    """
    Classe pour formater les données d'accélération
    """
    def __init__(self, df: pd.DataFrame):
        self.df = df
    
    def norm(self):
        """
        Calculer la norme du vecteur d'accélération
        """
        # Calculer la norme du vecteur d'accélération a = sqrt(x^2 + y^2 + z^2)
        self.df["acceleration (g)"] = np.sqrt(self.df["X (g)"]**2 + self.df["Y (g)"]**2 + self.df["Z (g)"]**2)
    
    def trim(self):
        """
        Réduire les données pour supprimer la première et la dernière seconde de l'enregistrement
        """
        first_sec = self.df.iloc[0]["Timestamp"]
        last_sec = self.df.iloc[-1]["Timestamp"]

        # Garder uniquement les données entre la première et la dernière seconde exclues
        self.df = self.df.query("Timestamp > @first_sec & Timestamp < @last_sec")
        self.df = self.df.reset_index(drop=True)
    
    def set_time(self):
        """
        Définir la colonne de temps pour qu'elle soit comptée en secondes depuis le début de l'enregistrement
        """
        self.df = self.df.copy()
        self.df['time (s)'] = 0
        self.df['time (s)'] = self.df['time (s)'].astype(float)
        group = self.df.groupby("Timestamp")

        for idx, (name, group_df) in enumerate(group):
            group_df["time (s)"] = idx + np.linspace(0, 1, len(group_df)+1)[:-1]

            self.df.update(group_df)

        self.df["time (s)"] = self.df["time (s)"].astype(float)
    
    def get_timestamp_precision(self):
        """
        Obtenir la précision des timestamps

        Returns:
            float: La précision des timestamps, 
            "s" si la précision est en secondes,
            "ms" si la précision est en millisecondes,
            "us" si la précision est en microsecondes
        """
        # Obtenir la différence entre deux timestamps consécutifs
        date = self.df["Timestamp"][0]
        if date.microsecond == 0:
            return "s"
        elif date.microsecond%1000 == 0:
            return "ms"
        else:
            return "us"
    
    def reinterpolate(self):
        """
        Réinterpoler les données pour avoir une fréquence de 100Hz
        """
        self.df['time (timedelta)'] = pd.to_timedelta(self.df['time (s)'], unit='s')
        self.df = self.df.set_index('time (timedelta)')
        self.df = self.df.resample('10ms').mean()
        self.df = self.df.interpolate(method='linear')
        self.df['time (s)'] = self.df.index.total_seconds()
    
    def process(self):
        """
        Appliquer les transformations sur le dataframe

        Returns:
            pd.DataFrame: Le dataframe transformé
        """
        self.df["Timestamp"] = pd.to_datetime(self.df["Timestamp"])
        self.norm()
        if self.get_timestamp_precision() == "s":
            self.trim()
            self.set_time()
        else:
            self.df['time (s)'] = (self.df["Timestamp"] - self.df["Timestamp"].iloc[0]).dt.total_seconds()
        self.df = self.df.drop(columns=["Timestamp"])
        cols = self.df.columns.tolist()
        cols = cols[-1:] + cols[:-1]
        self.df = self.df[cols]
        self.reinterpolate()

if __name__ == "__main__":
    input_path = glob.glob("./raw/*")
    # Les noms de chaque membre du groupe, associés aux chemins de leurs fichiers
    members_names = {os.path.basename(elt): elt for elt in input_path}

    for name, path in members_names.items():
        input_files = glob.glob(f"{path}/*")
        print(name)
        for f in input_files:
            df = pd.read_csv(f)
            print(f"Traitement de {f}")
            data = DataFormatting(df)
            data.process()
            df = data.df
            OUTPUT_DIR = f"./processed/{name}"
            if not os.path.exists(OUTPUT_DIR):
                os.makedirs(OUTPUT_DIR)
            df.to_csv(f"{OUTPUT_DIR}/{os.path.basename(f)}", index=False)

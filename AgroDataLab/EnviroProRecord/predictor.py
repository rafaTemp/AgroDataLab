import os
import joblib
import pandas as pd
from django.conf import settings

from .preparar_datos import preparar_dataset_para_modelo, FEATURES_FINAL


def cargar_modelo():
    ruta_modelo = os.path.join(
        settings.BASE_DIR,
        'EnviroProRecord',
        'ml_models',
        'modelo_random_forest_humedad_24reg.pkl'
    )

    if not os.path.exists(ruta_modelo):
        raise FileNotFoundError(f"No existe el modelo en: {ruta_modelo}")

    return joblib.load(ruta_modelo)


def predecir_humedad_baja(df_raw: pd.DataFrame) -> pd.DataFrame:
    """
    Recibe un DataFrame original, prepara los datos y añade predicción.
    """

    modelo = cargar_modelo()

    df_modelo = preparar_dataset_para_modelo(df_raw)

    X = df_modelo[FEATURES_FINAL]

    df_modelo['Prediccion_Humedad_Baja_24reg'] = modelo.predict(X)

    if hasattr(modelo, "predict_proba"):
        df_modelo['Probabilidad_Humedad_Baja_24reg'] = modelo.predict_proba(X)[:, 1]

    return df_modelo
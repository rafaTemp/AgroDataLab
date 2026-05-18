import os
import joblib
import pandas as pd
from django.conf import settings

from .preparar_datos import preparar_dataset_para_modelo, FEATURES_FINAL


MODELOS = {
    "random_forest": {
        "nombre": "Random Forest - Humedad baja 24 registros",
        "archivo": "modelo_random_forest_humedad_24reg.pkl",
    },
    "arbol_sin_bajon": {
        "nombre": "Árbol de decisión - Sin bajón de batería",
        "archivo": "modelo_arbol_final_sin_bajon_bateria.pkl",
    },
}


def cargar_modelo(modelo_id):
    info_modelo = MODELOS.get(modelo_id)

    if not info_modelo:
        raise ValueError("Modelo no válido.")

    ruta_modelo = os.path.join(
        settings.BASE_DIR,
        "EnviroProRecord",
        "ml_models",
        info_modelo["archivo"]
    )

    if not os.path.exists(ruta_modelo):
        raise FileNotFoundError(f"No existe el modelo en: {ruta_modelo}")

    modelo_cargado = joblib.load(ruta_modelo)

    if isinstance(modelo_cargado, dict):
        modelo = modelo_cargado["modelo"]
        features = modelo_cargado.get("features", FEATURES_FINAL)
    else:
        modelo = modelo_cargado
        features = FEATURES_FINAL

    return modelo, features, info_modelo["nombre"]


def predecir_humedad_baja(df_raw: pd.DataFrame, modelo_id="random_forest") -> pd.DataFrame:
    modelo, features, nombre_modelo = cargar_modelo(modelo_id)

    df_modelo = preparar_dataset_para_modelo(df_raw)

    X = df_modelo[features]

    df_modelo["Modelo_Usado"] = nombre_modelo
    df_modelo["Prediccion_Humedad_Baja_24reg"] = modelo.predict(X)

    if hasattr(modelo, "predict_proba"):
        df_modelo["Probabilidad_Humedad_Baja_24reg"] = modelo.predict_proba(X)[:, 1]
    else:
        df_modelo["Probabilidad_Humedad_Baja_24reg"] = None

    return df_modelo
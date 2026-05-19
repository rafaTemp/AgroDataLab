import pandas as pd


FEATURES_FINAL = [
    'Humedad_Media',
    'Humedad_Max',
    'Humedad_Min',
    'Temperatura_Media',
    'Temperatura_Max',
    'Temperatura_Min',
    'Bateria_mV',
    'Panel_Solar_mV',
    'Humedad_Diff_1',
    'Humedad_Rolling_3',
    'Humedad_Rolling_6',
    'Temperatura_Diff_1',
    'Bateria_Diff_1',
    'Panel_Solar_Diff_1'
]


def preparar_dataset_para_modelo(df_raw: pd.DataFrame) -> pd.DataFrame:
    df = df_raw.copy()

    if "Unnamed: 0" in df.columns and "Fecha_Hora" not in df.columns:
        df = df.rename(columns={"Unnamed: 0": "Fecha_Hora"})

    df = df[df["Fecha_Hora"] != "Fecha / Hora"].copy()
    df["Fecha_Hora"] = pd.to_datetime(df["Fecha_Hora"], errors="coerce")

    for col in df.columns:
        if col != "Fecha_Hora":
            df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna(subset=["Fecha_Hora"])
    df = df.sort_values("Fecha_Hora").reset_index(drop=True)

    # Si ya viene procesado
    if all(col in df.columns for col in FEATURES_FINAL):
        return df.dropna(subset=FEATURES_FINAL).reset_index(drop=True)

    columnas_humedad = [
        col for col in df.columns
        if "humedad" in col.lower() and "[%]" in col
    ]

    columnas_temperatura = [
        col for col in df.columns
        if "temperatura" in col.lower() and "promedio" not in str(df[col].iloc[0]).lower()
    ]

    col_bateria = next((c for c in df.columns if "bater" in c.lower()), None)
    col_panel = next((c for c in df.columns if "panel" in c.lower()), None)

    if not columnas_humedad:
        raise ValueError(f"No se encontraron columnas de humedad: {list(df.columns)}")

    if not columnas_temperatura:
        raise ValueError(f"No se encontraron columnas de temperatura: {list(df.columns)}")

    if col_bateria is None:
        raise ValueError(f"No se encontró columna batería: {list(df.columns)}")

    if col_panel is None:
        raise ValueError(f"No se encontró columna panel solar: {list(df.columns)}")

    df_modelo = pd.DataFrame({
        "Fecha_Hora": df["Fecha_Hora"],
        "Humedad_Media": df[columnas_humedad].mean(axis=1),
        "Humedad_Max": df[columnas_humedad].max(axis=1),
        "Humedad_Min": df[columnas_humedad].min(axis=1),
        "Temperatura_Media": df[columnas_temperatura].mean(axis=1),
        "Temperatura_Max": df[columnas_temperatura].max(axis=1),
        "Temperatura_Min": df[columnas_temperatura].min(axis=1),
        "Bateria_mV": df[col_bateria],
        "Panel_Solar_mV": df[col_panel],
    })

    df_modelo["Humedad_Diff_1"] = df_modelo["Humedad_Media"].diff()
    df_modelo["Humedad_Rolling_3"] = df_modelo["Humedad_Media"].rolling(3).mean()
    df_modelo["Humedad_Rolling_6"] = df_modelo["Humedad_Media"].rolling(6).mean()
    df_modelo["Temperatura_Diff_1"] = df_modelo["Temperatura_Media"].diff()
    df_modelo["Bateria_Diff_1"] = df_modelo["Bateria_mV"].diff()
    df_modelo["Panel_Solar_Diff_1"] = df_modelo["Panel_Solar_mV"].diff()

    return df_modelo.dropna(subset=FEATURES_FINAL).reset_index(drop=True)
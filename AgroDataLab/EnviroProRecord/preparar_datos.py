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
    """
    Recibe el dataset original con sensores EnviroPro y devuelve
    un DataFrame con las variables necesarias para el modelo Random Forest.
    """

    df = df_raw.copy()

    # Asegurar que tenemos una columna Fecha_Hora
    if 'Fecha_Hora' not in df.columns:
        # Si la primera columna se llama 'Unnamed: 0', 'Fecha', 'Date', etc., renombrarla
        posibles_nombres = ['Unnamed: 0', 'Fecha', 'Date', 'fecha', 'date', 'Fecha / Hora']
        for nombre in posibles_nombres:
            if nombre in df.columns:
                df = df.rename(columns={nombre: 'Fecha_Hora'})
                break
        else:
            # Si no encontramos ninguno conocido, intentamos con la primera columna
            df = df.rename(columns={df.columns[0]: 'Fecha_Hora'})

    # Eliminar posibles filas descriptivas
    df = df[df['Fecha_Hora'] != 'Fecha / Hora'].copy()

    # Convertir fecha
    df['Fecha_Hora'] = pd.to_datetime(df['Fecha_Hora'], errors='coerce')

    # Convertir columnas numéricas, manejando posible coma decimal
    for col in df.columns:
        if col != 'Fecha_Hora':
            if df[col].dtype == object:
                # Reemplazar coma por punto para poder convertir a numérico
                df[col] = df[col].astype(str).str.replace(',', '.')
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # Eliminar filas sin fecha
    df = df.dropna(subset=['Fecha_Hora'])

    if df.empty:
        raise ValueError("No hay datos válidos tras procesar las fechas. Revisa el formato del CSV.")

    # Ordenar
    df = df.sort_values('Fecha_Hora').reset_index(drop=True)

    # Detectar columnas
    columnas_humedad = [
        col for col in df.columns
        if 'sensor de humedad' in col.lower()
        and '[%]' in col
    ]

    columnas_temperatura = [
        col for col in df.columns
        if 'sensor de temperatura' in col.lower()
    ]

    if len(columnas_humedad) == 0:
        raise ValueError("Error de formato: No se han encontrado columnas de 'Sensor de humedad [%]' en el archivo.")

    if len(columnas_temperatura) == 0:
        raise ValueError("Error de formato: No se han encontrado columnas de 'Sensor de temperatura [ºC]' en el archivo.")

    # Buscar batería y panel de forma robusta
    col_bateria = next((c for c in df.columns if 'bater' in c.lower()), None)
    col_panel = next((c for c in df.columns if 'panel' in c.lower()), None)

    if not col_bateria:
        raise ValueError("Error de formato: No se encuentra la columna de nivel de batería.")
    if not col_panel:
        raise ValueError("Error de formato: No se encuentra la columna de carga del panel solar.")

    # Crear dataset unificado horario
    df_modelo = pd.DataFrame({
        'Fecha_Hora': df['Fecha_Hora'],

        'Humedad_Media': df[columnas_humedad].mean(axis=1),
        'Humedad_Max': df[columnas_humedad].max(axis=1),
        'Humedad_Min': df[columnas_humedad].min(axis=1),

        'Temperatura_Media': df[columnas_temperatura].mean(axis=1),
        'Temperatura_Max': df[columnas_temperatura].max(axis=1),
        'Temperatura_Min': df[columnas_temperatura].min(axis=1),

        'Bateria_mV': df[col_bateria],
        'Panel_Solar_mV': df[col_panel]
    })

    df_modelo = df_modelo.sort_values('Fecha_Hora').reset_index(drop=True)

    # Crear variables de tendencia iguales que en el entrenamiento
    df_modelo['Humedad_Diff_1'] = df_modelo['Humedad_Media'].diff()
    df_modelo['Humedad_Rolling_3'] = df_modelo['Humedad_Media'].rolling(3).mean()
    df_modelo['Humedad_Rolling_6'] = df_modelo['Humedad_Media'].rolling(6).mean()

    df_modelo['Temperatura_Diff_1'] = df_modelo['Temperatura_Media'].diff()
    df_modelo['Bateria_Diff_1'] = df_modelo['Bateria_mV'].diff()
    df_modelo['Panel_Solar_Diff_1'] = df_modelo['Panel_Solar_mV'].diff()

    # Quitar filas iniciales sin rolling/diff
    df_modelo = df_modelo.dropna(subset=FEATURES_FINAL).reset_index(drop=True)

    return df_modelo
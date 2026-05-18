def detectar_alertas_energia(df):
    alertas = []

    df = df.copy()
    df = df.sort_values("Fecha_Hora").reset_index(drop=True)

    df["Caida_Bateria"] = df["Bateria_mV"].diff()

    for _, fila in df.iterrows():
        fecha = fila["Fecha_Hora"]
        bateria = fila["Bateria_mV"]
        panel = fila["Panel_Solar_mV"]
        caida = fila["Caida_Bateria"]

        if bateria < 6000:
            alertas.append({
                "fecha": str(fecha),
                "tipo": "Batería crítica",
                "nivel": "Alta",
                "descripcion": f"La batería ha bajado a {bateria:.0f} mV.",
                "recomendacion": "Revisar batería, alimentación del nodo y conexión del sensor."
            })

        if caida < -300:
            alertas.append({
                "fecha": str(fecha),
                "tipo": "Caída brusca de batería",
                "nivel": "Media",
                "descripcion": f"Se detecta una caída brusca de batería de {abs(caida):.0f} mV.",
                "recomendacion": "Comprobar si hubo fallo de alimentación, desconexión o problema de carga."
            })

        if panel == 0 and bateria < 6300:
            alertas.append({
                "fecha": str(fecha),
                "tipo": "Panel solar sin carga y batería baja",
                "nivel": "Media",
                "descripcion": "El panel solar no está generando carga y la batería está baja.",
                "recomendacion": "Revisar orientación, suciedad, sombra o conexión del panel solar."
            })

    return alertas
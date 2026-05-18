from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import pandas as pd
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CSVUploadForm
import io
from .predictor import predecir_humedad_baja
from .analisis_energia import detectar_alertas_energia
from Alert.models import Alert
from Recommendation.models import Recommendation


@login_required
def inicio(request):
    return HttpResponse("Bienvenido a EnviroProRecord")


def importar_csv(request):
    if request.method == "POST":
        form = CSVUploadForm(request.POST, request.FILES)

        if form.is_valid():
            archivo = request.FILES["archivo_csv"]

            try:
                archivo_texto = io.TextIOWrapper(archivo.file, encoding="utf-8")
                df = pd.read_csv(archivo_texto, sep=None, engine="python")

                modelo_seleccionado = form.cleaned_data["modelo"]
                df_resultado = predecir_humedad_baja(df, modelo_seleccionado)

                request.session["modelo_seleccionado"] = modelo_seleccionado
                request.session["modelo_usado"] = df_resultado["Modelo_Usado"].iloc[0]

                alertas_energia = detectar_alertas_energia(df_resultado)

                request.session["alertas_energia"] = alertas_energia
                request.session["total_alertas_energia"] = len(alertas_energia)

                guardar_alertas_y_recomendaciones(alertas_energia)

                request.session["csv_columnas"] = list(df_resultado.columns)
                request.session["csv_filas"] = len(df_resultado)

                request.session["enviro_resultado"] = df_resultado.to_json(
                    orient="records",
                    date_format="iso"
                )

                messages.success(
                    request,
                    f"CSV cargado correctamente. Filas originales: {len(df)}. Filas procesadas: {len(df_resultado)}."
                )

                return redirect("resultado_enviro")

            except Exception as e:
                messages.error(request, f"Error al leer el CSV: {e}")

    else:
        form = CSVUploadForm()

    return render(request, "EnviroProRecord/importar_csv.html", {"form": form})


def resultado_enviro(request):
    datos_json = request.session.get("enviro_resultado")

    if not datos_json:
        messages.error(request, "Primero debes importar un CSV.")
        return redirect("importar_csv")

    df = pd.read_json(io.StringIO(datos_json))
    df["Fecha_Hora"] = pd.to_datetime(df["Fecha_Hora"])

    registros = df.tail(100).to_dict(orient="records")

    fechas = df["Fecha_Hora"].astype(str).tolist()
    humedad = df["Humedad_Media"].round(2).tolist()
    temperatura = df["Temperatura_Media"].round(2).tolist()
    probabilidad = df["Probabilidad_Humedad_Baja_24reg"].round(2).tolist()

    df["Anio"] = df["Fecha_Hora"].dt.year
    df["Mes"] = df["Fecha_Hora"].dt.to_period("M").astype(str)

    df_anual = df.groupby("Anio").agg({
        "Humedad_Media": "mean",
        "Temperatura_Media": "mean",
        "Probabilidad_Humedad_Baja_24reg": "mean"
    }).reset_index()

    df_mensual = df.groupby("Mes").agg({
        "Humedad_Media": "mean",
        "Temperatura_Media": "mean",
        "Probabilidad_Humedad_Baja_24reg": "mean"
    }).reset_index()

    contexto = {
        "registros": registros,
        "total_registros": len(df),

        "fechas": fechas,
        "humedad": humedad,
        "temperatura": temperatura,
        "probabilidad": probabilidad,

        "anios": df_anual["Anio"].astype(str).tolist(),
        "humedad_anual": df_anual["Humedad_Media"].round(2).tolist(),
        "temperatura_anual": df_anual["Temperatura_Media"].round(2).tolist(),
        "probabilidad_anual": df_anual["Probabilidad_Humedad_Baja_24reg"].round(2).tolist(),

        "meses": df_mensual["Mes"].tolist(),
        "humedad_mensual": df_mensual["Humedad_Media"].round(2).tolist(),
        "temperatura_mensual": df_mensual["Temperatura_Media"].round(2).tolist(),
        "probabilidad_mensual": df_mensual["Probabilidad_Humedad_Baja_24reg"].round(2).tolist(),

        "modelo_usado": request.session.get("modelo_usado", "Modelo no especificado"),
    }

    return render(request, "EnviroProRecord/resultado_enviro.html", contexto)

def energia_enviro(request):
    datos_json = request.session.get("enviro_resultado")

    if not datos_json:
        messages.error(request, "Primero debes importar un CSV.")
        return redirect("importar_csv")

    df = pd.read_json(io.StringIO(datos_json))
    df["Fecha_Hora"] = pd.to_datetime(df["Fecha_Hora"])

    df["Anio"] = df["Fecha_Hora"].dt.year
    df["Mes"] = df["Fecha_Hora"].dt.to_period("M").astype(str)

    df_mensual = df.groupby("Mes").agg({
        "Bateria_mV": "mean",
        "Panel_Solar_mV": "mean"
    }).reset_index()

    df_anual = df.groupby("Anio").agg({
        "Bateria_mV": "mean",
        "Panel_Solar_mV": "mean"
    }).reset_index()

    alertas_energia = request.session.get("alertas_energia", [])

    contexto = {
        "total_registros": len(df),

        "fechas": df["Fecha_Hora"].astype(str).tolist(),
        "bateria": df["Bateria_mV"].round(0).tolist(),
        "panel_solar": df["Panel_Solar_mV"].round(0).tolist(),

        "meses": df_mensual["Mes"].tolist(),
        "bateria_mensual": df_mensual["Bateria_mV"].round(0).tolist(),
        "panel_solar_mensual": df_mensual["Panel_Solar_mV"].round(0).tolist(),

        "anios": df_anual["Anio"].astype(str).tolist(),
        "bateria_anual": df_anual["Bateria_mV"].round(0).tolist(),
        "panel_solar_anual": df_anual["Panel_Solar_mV"].round(0).tolist(),

        "alertas_energia": alertas_energia,
        "total_alertas_energia": len(alertas_energia),
    }

    return render(request, "EnviroProRecord/energia_enviro.html", contexto)


def guardar_alertas_y_recomendaciones(alertas_energia):
    for alerta in alertas_energia:
        if alerta["tipo"] == "Batería crítica":
            tipo_bd = "Bateria_critica"
            variable = "Batería"
        elif alerta["tipo"] == "Caída brusca de batería":
            tipo_bd = "Caida_bateria"
            variable = "Batería"
        elif alerta["tipo"] == "Panel solar sin carga y batería baja":
            tipo_bd = "Panel_sin_carga"
            variable = "Panel solar"
        else:
            continue

        alerta_bd = Alert.objects.create(
            tipo_de_alerta=tipo_bd,
            descripcion=alerta["descripcion"],
            variable_afectada=variable
        )

        Recommendation.objects.create(
            titulo=f"Recomendación: {alerta['tipo']}",
            descripcion=alerta["recomendacion"],
            alerta=alerta_bd,
            prioridad=alerta["nivel"],
            estado="Pendiente"
        )
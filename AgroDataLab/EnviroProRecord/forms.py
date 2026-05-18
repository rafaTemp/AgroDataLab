from django import forms


MODELOS_DISPONIBLES = [
    ("random_forest", "Random Forest - Humedad baja 24 registros"),
    ("arbol_sin_bajon", "Árbol de decisión - Sin bajón de batería"),
]


class CSVUploadForm(forms.Form):
    archivo_csv = forms.FileField(
        label="Selecciona un archivo CSV",
        help_text="Sube el CSV original de EnviroPro."
    )

    modelo = forms.ChoiceField(
        label="Modelo predictivo",
        choices=MODELOS_DISPONIBLES,
        help_text="Selecciona el modelo que quieres aplicar al CSV."
    )
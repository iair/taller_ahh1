import pandas as pd
import numpy as np
import yaml
import json

def load_yaml_encodings(yaml_file_path: str) -> dict:
    """
    Carga un archivo YAML con codificaciones de preguntas.

    Parámetros:
    - yaml_file_path: Ruta al archivo YAML

    Retorna:
    - Un diccionario con la clave 'survey_responses' conteniendo la lista de preguntas y sus codificaciones
    """
    with open(yaml_file_path, 'r', encoding='utf-8') as file:
        yaml_data = yaml.safe_load(file)
    return {'survey_responses': yaml_data}
def process_survey_data(
    df: pd.DataFrame, 
    encoding_dict: dict, 
    one_hot_encoders: dict = None, 
    log_unmapped: bool = True
) -> pd.DataFrame:
    """
    Aplica codificación a los datos de una encuesta utilizando un diccionario de encoding personalizado.

    Soporta diferentes tipos de variables:
    - 'binary': valores como "Sí"/"No" codificados en 1/0.
    - 'ordinal': respuestas ordenadas codificadas como enteros.
    - 'categorical': respuestas únicas codificadas con letras o números, sin one-hot encoding.
    - 'multiselect': respuestas múltiples codificadas como columnas dummy (una por cada opción seleccionada).

    Parámetros:
    ----------
    df : pd.DataFrame
        DataFrame con las respuestas originales de la encuesta.

    encoding_dict : dict
        Diccionario con la clave 'survey_responses' que contiene una lista de preguntas.
        Cada entrada debe incluir:
        - 'question': nombre exacto de la columna en el DataFrame.
        - 'type': uno de 'binary', 'ordinal', 'categorical', 'multiselect'.
        - 'encoding': diccionario de mapeo de valores para esa pregunta.

    one_hot_encoders : dict, opcional
        Estructura para registrar las columnas creadas por codificación multiselect. Por defecto es None.

    log_unmapped : bool, opcional
        Si es True, imprime advertencias para los valores no encontrados en el encoding
        y guarda un archivo 'unmapped_values.json' con el resumen.

    Retorna:
    -------
    pd.DataFrame
        Una copia del DataFrame original, con las columnas codificadas según las reglas provistas.
        Las columnas originales pueden ser reemplazadas o expandidas según su tipo.

    Efectos secundarios:
    --------------------
    - Muestra advertencias para preguntas no encontradas.
    - Imprime valores no mapeados y los guarda en 'unmapped_values.json' si log_unmapped es True.
    """
    if one_hot_encoders is None:
        one_hot_encoders = {}

    df = df.copy()
    unmapped_values = {}

    for question in encoding_dict['survey_responses']:
        question_text = question['question']
        encoding_type = question['type']
        encoding = question.get('encoding', {})

        if question_text not in df.columns:
            print(f"⚠️ Pregunta no encontrada en el DataFrame: '{question_text}'")
            continue

        if encoding_type in ("binary", "ordinal"):
            unmapped_values[question_text] = []

            def map_and_warn(x):
                val = str(x).strip() if pd.notna(x) else None
                if val is None:
                    return pd.NA
                if val not in encoding:
                    if log_unmapped:
                        print(f"⚠️  Valor no mapeado en '{question_text}': '{val}'")
                    unmapped_values[question_text].append(val)
                    return pd.NA
                return encoding[val]

            df[question_text] = df[question_text].apply(map_and_warn)

        elif encoding_type == "categorical":
            if not encoding:
                print(f"⚠️  Sin encoding definido para '{question_text}', se omite.")
                continue

            df[question_text] = df[question_text].apply(
                lambda x: encoding.get(str(x).strip(), pd.NA) if pd.notna(x) else pd.NA
            )

        elif encoding_type == "multiselect":
            if not encoding:
                print(f"⚠️  Sin encoding definido para '{question_text}', se omite.")
                continue

            for category_key, category_code in encoding.items():
                col_name = f"{question_text}__{category_code}"
                df[col_name] = df[question_text].apply(
                    lambda x: category_key in str(x).split(', ') if pd.notna(x) else False
                ).astype(int)
            df.drop(columns=[question_text], inplace=True)

        else:
            print(f"⚠️ Tipo de codificación desconocido: '{encoding_type}' en '{question_text}'")
            continue

    if log_unmapped:
        for question, values in unmapped_values.items():
            unique_unmapped = set(values)
            if unique_unmapped:
                print(f"\nResumen no mapeado en: {question}")
                print(f"Valores únicos no mapeados ({len(unique_unmapped)}): {unique_unmapped}")

        if any(unmapped_values.values()):
            import json
            with open("unmapped_values.json", "w", encoding="utf-8") as f:
                json.dump(unmapped_values, f, ensure_ascii=False, indent=2)
            print("\n🔍 Detalles guardados en: unmapped_values.json")

    return df
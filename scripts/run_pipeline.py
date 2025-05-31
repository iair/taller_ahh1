import pandas as pd
from taller_utils.encoding import load_yaml_encodings, process_survey_data

# Cargar los datos crudos (ajusta la ruta según corresponda)
df = pd.read_csv("data/raw/encuesta.csv")

# Cargar el diccionario de codificación
encoding_dict = load_yaml_encodings("data/raw/encodings.yaml")  # o diccionario .json adaptado si es el caso

# Procesar los datos
df_encoded = process_survey_data(df, encoding_dict)

# Guardar resultados
df_encoded.to_csv("data/processed/encuesta_codificada.csv", index=False)

print("✅ Codificación finalizada. Archivo guardado en data/processed/encuesta_codificada.csv")
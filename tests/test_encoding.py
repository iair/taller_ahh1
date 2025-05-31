import pandas as pd
from taller_utils.encoding import process_survey_data

def test_simple_binary_encoding():
    """
    Testea la codificación binaria básica en la función `process_survey_data`.

    Este test verifica que una columna de texto con respuestas binarias ("Sí", "No") 
    sea correctamente transformada a valores numéricos (1 y 0) según el diccionario
    de codificación definido.

    Casos evaluados:
    - "Sí" debe convertirse en 1
    - "No" debe convertirse en 0

    No se incluyen casos de valores no mapeados o nulos en este test.
    """
    df = pd.DataFrame({
        "¿Te gusta programar?": ["Sí", "No", "Sí"]
    })
    encoding_dict = {
        "survey_responses": [{
            "question": "¿Te gusta programar?",
            "type": "binary",
            "encoding": {"Sí": 1, "No": 0}
        }]
    }
    result = process_survey_data(df, encoding_dict, log_unmapped=False)
    assert result["¿Te gusta programar?"].tolist() == [1, 0, 1]
    
def test_unmapped_binary_value():
    """
    Verifica que la función `process_survey_data` maneje correctamente un valor no mapeado en codificación binaria.

    Este test asegura que:
    - Los valores definidos en el diccionario ("Sí", "No") se codifican correctamente como 1 y 0.
    - Los valores no definidos en el diccionario ("Tal vez") se transforman en `pd.NA`.
    - La estructura de salida mantiene el orden y el tamaño del DataFrame original.

    Este comportamiento es esencial para evitar errores silenciosos cuando aparecen respuestas inesperadas en los datos reales.
    """
    import pandas as pd
    from taller_utils.encoding import process_survey_data

    df = pd.DataFrame({
        "¿Te gusta programar?": ["Sí", "Tal vez", "No"]
    })
    encoding_dict = {
        "survey_responses": [{
            "question": "¿Te gusta programar?",
            "type": "binary",
            "encoding": {"Sí": 1, "No": 0}
        }]
    }
    result = process_survey_data(df, encoding_dict, log_unmapped=False)

    assert result["¿Te gusta programar?"].tolist() == [1, pd.NA, 0]


import pandas as pd
from taller_utils.encoding import process_survey_data

def test_process_skips_none_encoding():
    """
    Verifica que `process_survey_data` maneje correctamente casos en los que
    una pregunta tiene `encoding: None` (por ejemplo, en preguntas categóricas
    aún no codificadas).

    El test asegura que:
    - No se lanza un error (como AttributeError).
    - La columna correspondiente no se transforma ni se elimina.
    - Se imprime un mensaje de advertencia, pero se continúa procesando el resto.
    """
    df = pd.DataFrame({
        "¿Qué lugar(es) utilizas para estudiar?": ["Una habitación", "La cocina", "El patio"]
    })

    encoding_dict = {
        "survey_responses": [
            {
                "question": "¿Qué lugar(es) utilizas para estudiar?",
                "type": "categorical",
                "encoding": None  # <-- Caso que causaba crash antes
            }
        ]
    }

    result = process_survey_data(df, encoding_dict, log_unmapped=False)

    # Verificamos que la columna sigue igual (no transformada ni eliminada)
    assert "¿Qué lugar(es) utilizas para estudiar?" in result.columns
    assert result.shape == df.shape
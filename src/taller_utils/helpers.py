from datetime import datetime
def calculate_age(birth_date_str: str):
    """
    Calcula la edad de una persona a partir de su fecha de nacimiento en formato 'dd/mm/yyyy'.

    Parámetros:
    ----------
    birth_date_str : str
        Fecha de nacimiento como string en el formato 'día/mes/año' (por ejemplo, '25/12/2000').

    Retorna:
    -------
    int o None
        Edad en años si la conversión y cálculo son exitosos. 
        Devuelve None si ocurre un error en el parseo (formato inválido o valor nulo).

    Notas:
    ------
    - La edad se calcula con base en la fecha actual (hoy).
    - Si la fecha es inválida o no cumple el formato esperado, se ignora silenciosamente devolviendo None.
    """
    try:
        birth_date = datetime.strptime(birth_date_str, '%d/%m/%Y')
        today = datetime.now()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        return age
    except:
        return None

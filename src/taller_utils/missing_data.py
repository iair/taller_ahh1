import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency
def test_missing_mcar(df: pd.DataFrame, alpha: float = 0.01) -> None:
    """
    Evalúa si los datos faltantes en un DataFrame son MCAR (Missing Completely At Random)
    usando una prueba de chi-cuadrado sobre los patrones de valores faltantes.

    El procedimiento agrupa filas por patrón de missing values y evalúa si los patrones son independientes,
    lo que indicaría que los datos están completamente al azar.

    Parámetros:
    ----------
    df : pd.DataFrame
        DataFrame sobre el que se desea evaluar el patrón de valores faltantes.

    alpha : float, opcional
        Nivel de significancia para la prueba de hipótesis (por defecto 0.01).

    Retorna:
    -------
    None
        Imprime en consola:
        - Estadístico Chi²
        - Valor p
        - Grados de libertad
        - Frecuencias esperadas
        - Interpretación de si se rechaza o no la hipótesis nula (MCAR)

    Notas:
    ------
    - Si hay menos de dos patrones únicos de valores faltantes, la prueba no se puede realizar.
    - La hipótesis nula es que los datos faltantes están completamente al azar (MCAR).
    - Un valor p bajo indica que los datos no son MCAR.
    """
    df.replace("", np.nan, inplace=True)
    missing_patterns = df.isnull().astype(int)
    missing_patterns['pattern'] = missing_patterns.apply(lambda row: ''.join(row.astype(str)), axis=1)
    grouped = df.groupby(missing_patterns['pattern'])
    observed = grouped.size()
    if len(observed) < 2:
        print("Not enough unique missing patterns to perform a chi-squared test.")
        return
    contingency_table = np.array(observed).reshape(-1, 1)
    chi2, p_value, dof, expected = chi2_contingency(contingency_table, correction=False)
    print(f"Chi2 Statistic: {chi2}")
    print(f"P-value: {p_value}")
    print(f"Degrees of Freedom: {dof}")
    print(f"Expected Frequencies: {expected.flatten()}")
    if p_value > alpha:
        print("Result: Cannot reject the null hypothesis. The missing data is MCAR.")
    else:
        print("Result: Reject the null hypothesis. The missing data is not MCAR.")

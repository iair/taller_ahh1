import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import mannwhitneyu, chi2_contingency, fisher_exact, power_divergence

def explorar_relacion_con_target(df, pregunta, target):
    """
    Analiza la relación entre una variable de encuesta y una variable objetivo binaria.

    Esta función permite explorar preguntas individuales del dataset codificado en relación
    con la variable target. Dependiendo del tipo de variable, aplica:

    - Visualizaciones específicas:
        - Gráficos de barras apiladas para ordinales discretas o categóricas.
        - Boxplots para variables numéricas u ordinales continuas.
        - Barras horizontales para preguntas tipo multiselect codificadas como múltiples columnas dummy.

    - Pruebas estadísticas:
        - Mann–Whitney U test: para variables ordinales o numéricas.
        - Chi² test: para variables categóricas.
        - Fisher's exact test: si es tabla 2x2 y contiene frecuencias esperadas < 5.
        - G-test (log-likelihood): para tablas mayores a 2x2 con celdas esperadas < 5.

    Parámetros
    ----------
    df : pd.DataFrame
        DataFrame codificado con las respuestas de la encuesta.
    
    pregunta : str
        Nombre exacto de la columna (para preguntas simples) o prefijo (para preguntas multiselect).

    target : str
        Nombre de la columna objetivo binaria (0: no, 1: sí).

    Retorna
    -------
    None
        Muestra visualizaciones y estadísticas por pantalla. No retorna objetos.
    
    Notas
    -----
    - Las preguntas multiselect deben estar codificadas como columnas dummy con el patrón: `pregunta__codigo`.
    - Para preguntas categóricas con muchas categorías o con baja frecuencia por categoría, se recomienda revisar las advertencias de validez estadística.
    """

    if target not in df.columns:
        print(f"⚠️ Target '{target}' no encontrado.")
        return

    columnas_multi = [col for col in df.columns if col.startswith(f"{pregunta}__")]

    if columnas_multi:
        print(f"🔀 Pregunta multiselect detectada: {pregunta}")
        medios = df.groupby(target)[columnas_multi].mean().T
        medios.columns = ["No (0)", "Sí (1)"]
        medios.plot(kind="barh", figsize=(10, len(columnas_multi) * 0.5))
        plt.title(f"Proporción de uso por grupo del target\n{pregunta}")
        plt.xlabel("Proporción")
        plt.ylabel("Opción seleccionada")
        plt.grid(axis="x", linestyle="--", alpha=0.6)
        plt.tight_layout()
        plt.show()
        return

    if pregunta not in df.columns:
        print(f"⚠️ Pregunta '{pregunta}' no encontrada.")
        return

    serie = df[pregunta]

    if pd.api.types.is_numeric_dtype(serie):
        print(f"📈 Análisis numérico/ordinal para: {pregunta}")

        resumen = df.groupby(target)[pregunta].describe()
        print(resumen)

        unique_vals = sorted(serie.dropna().unique())
        is_discrete_ordinal = all(float(x).is_integer() for x in unique_vals) and len(unique_vals) <= 10

        if is_discrete_ordinal:
            tabla = pd.crosstab(df[pregunta], df[target], normalize='index') * 100
            tabla.plot(kind='bar', stacked=True, figsize=(8, 5), colormap="Paired")
            plt.title(f"Distribución de respuestas por grupo del target\n{pregunta}")
            plt.xlabel("Respuesta ordinal")
            plt.ylabel("Porcentaje")
            plt.legend(title="Target", labels=["No (0)", "Sí (1)"])
            plt.tight_layout()
            plt.show()

        sns.boxplot(data=df, x=target, y=pregunta)
        plt.title(f"Distribución de '{pregunta}' según target")
        plt.grid(axis="y", linestyle="--", alpha=0.6)
        plt.tight_layout()
        plt.show()

        g0 = df[df[target] == 0][pregunta].dropna()
        g1 = df[df[target] == 1][pregunta].dropna()
        stat, p = mannwhitneyu(g0, g1, alternative="two-sided")
        print(f"Mann–Whitney U test: U = {stat:.2f}, p = {p:.4f}")

    else:
        print(f"📊 Análisis categórico para: {pregunta}")

        tabla = pd.crosstab(df[pregunta], df[target], normalize='index') * 100
        tabla.plot(kind='barh', stacked=True, figsize=(10, 6), colormap="Paired")
        plt.title(f"Distribución de respuestas en '{pregunta}' por target")
        plt.xlabel("Porcentaje")
        plt.ylabel("Respuesta")
        plt.legend(title="Target", labels=["No (0)", "Sí (1)"])
        plt.tight_layout()
        plt.show()

        contingencia = pd.crosstab(df[pregunta], df[target])
        chi2, p_chi2, dof, expected = chi2_contingency(contingencia)

        if (expected < 5).any():
            print("⚠️ Advertencia: algunas frecuencias esperadas son menores a 5, lo que puede afectar la validez del test de Chi-cuadrado.")

            if expected.shape == (2, 2):
                print("ℹ️ Se aplica test exacto de Fisher para mayor precisión en tabla 2x2.")
                _, fisher_p = fisher_exact(contingencia)
                print(f"Fisher exact test: p-value = {fisher_p:.4f}")
            else:
                print("ℹ️ Se aplica G-test (power divergence) como alternativa.")
                g_stat, g_p = power_divergence(contingencia.values, lambda_='log-likelihood')
                g_stat_val = float(np.asarray(g_stat).flatten()[0])
                g_p_val = float(np.asarray(g_p).flatten()[0])
                print(f"G-test (log-likelihood): G = {g_stat_val:.2f}, p-value = {g_p_val:.4f}")

        else:
            print(f"Chi² test: χ² = {chi2:.2f}, p-value = {p_chi2:.4f}")

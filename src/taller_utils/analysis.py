import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import mannwhitneyu, chi2_contingency

def explorar_relacion_con_target(df, pregunta, target):
    """
    Explora la relación entre una pregunta (columna individual o multiselect) y el target.

    - Detecta tipo: numérica, categórica o multiselect.
    - Aplica análisis visual y estadístico adecuado.
    - Soporta preguntas multiselect codificadas como columnas dummy con prefijo común.

    Parámetros:
    - df: DataFrame codificado.
    - pregunta: string (nombre exacto de columna o prefijo para multiselect).
    - target: nombre de la columna target binaria (0/1).
    """
    # Validación básica
    if target not in df.columns:
        print(f"⚠️ Target '{target}' no encontrado.")
        return
    
    # Caso 1: multiselect (prefijo con columnas dummy)
    columnas_multi = [col for col in df.columns if col.startswith(f"{pregunta}__")]

    if columnas_multi:
        print(f"🔀 Pregunta multiselect detectada: {pregunta}")
        medios = df.groupby(target)[columnas_multi].mean().T
        medios.columns = ["No (0)", "Sí (1)"]
        medios.plot(kind="barh", figsize=(10, len(columnas_multi)*0.5))
        plt.title(f"Proporción de uso por grupo del target\n{pregunta}")
        plt.xlabel("Proporción")
        plt.ylabel("Opción seleccionada")
        plt.grid(axis="x", linestyle="--", alpha=0.6)
        plt.tight_layout()
        plt.show()
        return

    # Caso 2: columna simple (numérica o categórica)
    if pregunta not in df.columns:
        print(f"⚠️ Pregunta '{pregunta}' no encontrada.")
        return

    serie = df[pregunta]
    
    # Detectar si es numérica/ordinal
    if pd.api.types.is_numeric_dtype(serie):
        print(f"📈 Análisis numérico/ordinal para: {pregunta}")

        resumen = df.groupby(target)[pregunta].describe()
        print(resumen)

        unique_vals = sorted(serie.dropna().unique())
        is_discrete_ordinal = all(float(x).is_integer() for x in unique_vals) and len(unique_vals) <= 10

        if is_discrete_ordinal:
            # Barras apiladas
            tabla = pd.crosstab(df[pregunta], df[target], normalize='index') * 100
            tabla.plot(kind='bar', stacked=True, figsize=(8, 5), colormap="Paired")
            plt.title(f"Distribución de respuestas por grupo del target\n{pregunta}")
            plt.xlabel("Respuesta ordinal")
            plt.ylabel("Porcentaje")
            plt.legend(title="Target", labels=["No (0)", "Sí (1)"])
            plt.tight_layout()
            plt.show()

        # Boxplot por grupo
        sns.boxplot(data=df, x=target, y=pregunta)
        plt.title(f"Distribución de '{pregunta}' según target")
        plt.grid(axis="y", linestyle="--", alpha=0.6)
        plt.tight_layout()
        plt.show()

        # Mann–Whitney U test
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

        # Chi-cuadrado
        contingencia = pd.crosstab(df[pregunta], df[target])
        if (contingencia.values < 5).any():
            print("⚠️ Precaución: algunas frecuencias son < 5. Chi² puede ser inestable.")
        chi2, p, _, _ = chi2_contingency(contingencia)
        print(f"Chi² test: χ²={chi2:.2f}, p-value={p:.4f}")
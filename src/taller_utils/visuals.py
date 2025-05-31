import pandas as pd
import matplotlib.pyplot as plt

def plot_distribution(
   df: pd.DataFrame, 
   variable_name: str, 
   question_text: str = None, 
   ascending: bool = False, 
   rotation: int = 0,
   horizontal: bool = True,
   figsize: tuple = (8, 6)
) -> None:
    """
    Genera un gráfico de barras para visualizar la distribución de una variable categórica u ordinal.

    Parámetros:
    ----------
    df : pd.DataFrame
        DataFrame que contiene los datos.

    variable_name : str
        Nombre de la columna a visualizar.

    question_text : str, opcional
        Texto descriptivo de la pregunta para usar en el título del gráfico. 
        Si no se proporciona, se usa el nombre de la columna.

    ascending : bool, opcional
        Si True, ordena los valores del gráfico en orden ascendente. Por defecto es False.

    rotation : int, opcional
        Ángulo de rotación para las etiquetas de los ejes. Útil si las categorías tienen nombres largos.

    horizontal : bool, opcional
        Si True, el gráfico será horizontal (barh); si False, será vertical (bar). Por defecto es horizontal.

    figsize : tuple, opcional
        Tamaño de la figura en pulgadas como (ancho, alto). Si el gráfico es vertical, se invierte automáticamente.

    Retorna:
    -------
    None
        Muestra el gráfico directamente usando matplotlib.pyplot.
    """
    target_counts = df[variable_name].value_counts().sort_index(ascending=ascending)
    title_text = question_text if question_text else f'Distribution for {variable_name}'

    plt.figure(figsize=figsize if horizontal else figsize[::-1])
    target_counts.plot(
        kind='barh' if horizontal else 'bar',
        color=['skyblue', 'salmon'], 
        edgecolor='black'
    )

    plt.title(f'Distribución para: {title_text} ({variable_name})', fontsize=16)
    if horizontal:
        plt.xlabel('Cantidad', fontsize=14)
        plt.ylabel(f'{variable_name} Categorías', fontsize=14)
    else:
        plt.xlabel(f'{variable_name} Categorías', fontsize=14)
        plt.ylabel('Cantidad', fontsize=14)
        
    plt.xticks(rotation=rotation)
    plt.grid(axis='x' if horizontal else 'y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()
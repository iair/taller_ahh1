import pandas as pd
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency

def plot_distribution(df: pd.DataFrame, variable_name : str, question_text:str=None)->None:
    """
    Plot the distribution of a given variable in a DataFrame.
    
    Parameters:
    - df: DataFrame containing the data.
    - variable_name: Column name of the variable to plot.
    - question_text: Optional. The text of the question to display as the title.
    
    Returns:
    - A bar plot showing the distribution of the variable.
    """
    # Calculate the value counts
    target_counts = df[variable_name].value_counts()
    
    # Use the provided question text or default to the variable name
    title_text = question_text if question_text else f'Distribution for {variable_name}'
    
    # Plot the distribution
    plt.figure(figsize=(8, 6))
    target_counts.plot(kind='bar', color=['skyblue', 'salmon'], edgecolor='black')
    plt.title(f'Distribución para: {title_text} ({variable_name})', fontsize=16)
    plt.xlabel(f'{variable_name} Categorías', fontsize=14)
    plt.ylabel('Cantidad', fontsize=14)
    plt.xticks(rotation=0)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

def test_missing_mcar(df: pd.DataFrame, alpha: float = 0.01) -> None:
    """
    Test whether missing data in a DataFrame is Missing Completely At Random (MCAR)
    using a chi-squared test based on missing value patterns.

    Parameters:
    - df (pd.DataFrame): The DataFrame to analyze.
    - alpha (float): Significance level for the chi-squared test. Default is 0.01.

    Returns:
    - None: Prints the results of the chi-squared test, including the chi-squared statistic,
            p-value, degrees of freedom, and whether the null hypothesis of MCAR can be rejected.
    """
    # Identify missing value patterns as binary indicators (1 for missing, 0 for not missing)
    missing_patterns = df.isnull().astype(int)

    # Convert missing patterns to unique strings for grouping
    missing_patterns['pattern'] = missing_patterns.apply(lambda row: ''.join(row.astype(str)), axis=1)

    # Group the original DataFrame by missing patterns
    grouped = df.groupby(missing_patterns['pattern'])

    # Calculate observed frequencies for each missing pattern
    observed = grouped.size()

    # Create a contingency table from observed frequencies
    contingency_table = np.array(observed).reshape(-1, 1)

    # Perform the chi-squared test
    chi2, p_value, dof, expected = chi2_contingency(contingency_table, correction=False)

    # Print test results
    print(f"Chi2 Statistic: {chi2}")
    print(f"P-value: {p_value}")
    print(f"Degrees of Freedom: {dof}")
    print(f"Expected Frequencies: {expected.flatten()}")

    # Interpret the p-value
    if p_value > alpha:
        print("Result: Cannot reject the null hypothesis. The missing data is MCAR.")
    else:
        print("Result: Reject the null hypothesis. The missing data is not MCAR.")

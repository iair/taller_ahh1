import pandas as pd
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency
from sklearn.preprocessing import OneHotEncoder
import yaml
from datetime import datetime

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
   Plot distribution with optional sorting and orientation.
   
   Parameters:
   - df: DataFrame containing the data
   - variable_name: Column name to plot 
   - question_text: Optional title text
   - ascending: Sort bars ascending if True
   - rotation: Rotation angle for labels
   - horizontal: If True, horizontal bars; if False, vertical
   - figsize: Figure size tuple (width, height)
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
    # Ensure placeholders for missing data are replaced with np.nan
    df.replace("", np.nan, inplace=True)

    # Identify missing value patterns as binary indicators (1 for missing, 0 for not missing)
    missing_patterns = df.isnull().astype(int)

    # Convert missing patterns to unique strings for grouping
    missing_patterns['pattern'] = missing_patterns.apply(lambda row: ''.join(row.astype(str)), axis=1)

    # Group the original DataFrame by missing patterns
    grouped = df.groupby(missing_patterns['pattern'])

    # Calculate observed frequencies for each missing pattern
    observed = grouped.size()

    # Check if there are enough unique patterns for a chi-squared test
    if len(observed) < 2:
        print("Not enough unique missing patterns to perform a chi-squared test.")
        return

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
        
def calculate_age(birth_date_str):
   try:
       birth_date = datetime.strptime(birth_date_str, '%d/%m/%Y')
       today = datetime.now()
       age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
       return age
   except:
       return None
        
def load_yaml_encodings(yaml_file_path: str) -> dict:
    """
    Loads survey encoding rules from a YAML file.
    Returns a dictionary compatible with process_survey_data.
    """
    with open(yaml_file_path, 'r', encoding='utf-8') as file:
        yaml_data = yaml.safe_load(file)
    return {'survey_responses': yaml_data}

def process_survey_data(
    df: pd.DataFrame, 
    encoding_dict: dict, 
    one_hot_encoders: dict = None, 
    ohe_categorical: bool = False
) -> pd.DataFrame:
    """
    Processes survey data based on a given encoding dictionary.

    Parameters:
    - df (pd.DataFrame): The survey data to process.
    - encoding_dict (dict): The dictionary containing encoding rules from YAML.
    - one_hot_encoders (dict): Dictionary to store OneHotEncoders for categorical variables.
    - ohe_categorical (bool): If True, apply one-hot encoding to categorical variables.
                            If False, replace categorical values with letters.

    Returns:
    - pd.DataFrame: The processed DataFrame.
    """
    if one_hot_encoders is None:
        one_hot_encoders = {}
    
    df = df.copy()
    unmapped_values = {}  # Guarda respuestas no encontradas por pregunta
    
    for question in encoding_dict['survey_responses']:
        question_text = question['question']
        encoding_type = question['type']
        encoding = question['encoding']

        if question_text not in df.columns:
            print(f'Warning: Question not found in survey: {question_text}')
            continue

        if encoding_type in ('binary', 'ordinal'):
            unmapped_values[question_text] = []

            def map_and_warn(x):
                val = str(x).strip() if pd.notna(x) else None
                if val is None:
                    return pd.NA
                if val not in encoding:
                    print(f"⚠️  Valor no mapeado en '{question_text}': '{val}'")
                    unmapped_values[question_text].append(val)
                    return pd.NA
                return encoding[val]

            df[question_text] = df[question_text].apply(map_and_warn)

        elif encoding_type == 'categorical':
            if ohe_categorical:
                try:
                    # Split multiple responses
                    responses = df[question_text].str.split(', ').explode().str.strip()
                    # Convert to categorical with all expected categories (even if missing in data)
                    responses = pd.Categorical(responses, categories=encoding.keys())
                    # Create dummy variables including all expected categories
                    dummies = pd.get_dummies(responses, prefix=question_text)
                    # Aggregate dummy columns back to original index
                    encoded = dummies.groupby(level=0).max()
                    # Fill missing columns (those not present in data but in encoding)
                    expected_cols = [f"{question_text}_{cat}" for cat in encoding.keys()]
                    for col in expected_cols:
                        if col not in encoded.columns:
                            encoded[col] = 0
                    encoded = encoded[expected_cols]  # Ensure column order
                    # Store encoder information
                    one_hot_encoders[question_text] = {
                        'categories': list(encoding.keys()),
                        'encoded_columns': encoded.columns
                    }
                    # Update DataFrame
                    df = df.drop(columns=[question_text]).join(encoded)
                except Exception as e:
                    print(f'Error one-hot encoding {question_text}: {str(e)}')
                    continue
            else:
                # Handle multiple responses for categorical variables
                for category_key, category_code in encoding.items():
                    col_name = f"{question_text}__{category_code}"
                    df[col_name] = df[question_text].apply(
                        lambda x: category_key in str(x).split(', ') if pd.notna(x) else False
                    ).astype(int)
                df.drop(columns=[question_text], inplace=True)
        
    # Mostrar resumen de valores no mapeados
    for question, values in unmapped_values.items():
        unique_unmapped = set(values)
        if unique_unmapped:
            print(f"\nResumen no mapeado en: {question}")
            print(f"Valores únicos no mapeados ({len(unique_unmapped)}): {unique_unmapped}")

    # Guardar a archivo JSON si hubo errores
    if any(unmapped_values.values()):
        import json
        with open("unmapped_values.json", "w", encoding="utf-8") as f:
            json.dump(unmapped_values, f, ensure_ascii=False, indent=2)
        print("\n🔍 Detalles guardados en: unmapped_values.json")


    return df
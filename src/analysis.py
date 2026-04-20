import pandas as pd
from scipy.stats import f_oneway, ttest_ind
from itertools import combinations

def full_statistical_analysis(file_path):

    """
    Perform comprehensive statistical analysis on hematological parameters 
    grouped by genotype.

    This function conducts a one-way Analysis of Variance (ANOVA) across all 
    available genotype groups to determine whether statistically significant 
    differences exist among them. It then performs automatic pairwise 
    independent two-sample t-tests (Welch’s t-test) between all possible 
    genotype combinations.

    The results are returned as structured pandas DataFrames suitable for 
    academic reporting and further analysis.

    Parameters
    ----------
    file_path : str
        Path to the input CSV file containing the dataset. The dataset must 
        include a 'Genotype' column and the following numerical columns:
        ['Hb', 'PCV', 'MCV', 'MCH', 'MCHC', 'RBC', 'TWBC', 'Platelets'].

    Returns
    -------
    dict
        A dictionary containing:
        
        - "ANOVA" : pandas.DataFrame
            A table with columns:
            ['Parameters', 'F-value', 'P-value'], showing results of the 
            one-way ANOVA for each parameter.
        
        - "T-TESTS" : dict of pandas.DataFrame
            A dictionary where each key represents a pairwise comparison 
            (e.g., 'AA_vs_SS'), and each value is a DataFrame with columns:
            ['Parameters', '<Group1> (n = x)', '<Group2> (n = y)', 
             'T-test', 'P-value'].

    Raises
    ------
    FileNotFoundError
        If the specified file_path does not exist.

    KeyError
        If required columns (e.g., 'Genotype' or parameter columns) are missing.

    ValueError
        If the dataset does not contain at least two genotype groups for analysis.

    Notes
    -----
    - ANOVA is used to test the null hypothesis that all group means are equal.
    - Welch’s t-test (independent samples, unequal variance) is used for 
      pairwise comparisons.
    - A p-value < 0.05 is typically considered statistically significant.
    - Multiple pairwise comparisons may increase Type I error; consider applying 
      correction methods such as Bonferroni or Tukey HSD if required.

    Examples
    --------
    >>> results = full_statistical_analysis("data.csv")
    >>> results["ANOVA"]
    >>> results["T-TESTS"]["AA_vs_SS"]
    """
    # Load dataset
    df = pd.read_csv(file_path)
    
    # Parameters
    parameters = ['Hb', 'PCV', 'MCV', 'MCH', 'MCHC', 'RBC', 'TWBC', 'Platelets']

    # Group statistics (mean & std)
    stats = df.groupby('Genotype')[parameters].agg(['mean', 'std'])
    
    # Available genotypes
    genotypes = df['Genotype'].dropna().unique()
    
    # ---------------------------
    # ANOVA TABLE
    # ---------------------------
    anova_data = {
        'Parameters': [],
        'AA': [],
        'AS': [],
        'SS': [],
        'F-value': [],
        'P-value': []
    }
    
    # loop through each parameter
    for param in parameters:
        # Store mean ± std for each genotype
        groups = {}

        for genotype in genotypes:
            if genotype in stats.index:
                mean_val = stats.loc[genotype, (param, 'mean')]
                std_val = stats.loc[genotype, (param, 'std')]
                
                anova_data[genotype].append(f"{mean_val:.2f} ± {std_val:.2f}")
                
                # Collect raw data for ANOVA
                groups = [df[df['Genotype'] == g][param].dropna() for g in genotypes]
            else:
                anova_data[genotype].append("N/A")
        
        # perform ANOVA (only if at least 2 groups exist)
        if len(groups) >= 2:
            f_val, p_val = f_oneway(*groups)
        else:
            f_val, p_val = None, None
        
        anova_data['Parameters'].append(param)
        anova_data['F-value'].append(f"{f_val:.4f}" if f_val else "N/A")
        anova_data['P-value'].append(f"{p_val:.4f}" if p_val else "N/A")
    
    anova_table = pd.DataFrame(anova_data)
    
    # ---------------------------
    # PAIRWISE T-TESTS
    # ---------------------------
    ttest_tables = {}
    
    for g1, g2 in combinations(genotypes, 2):
        g1_data = df[df['Genotype'] == g1]
        g2_data = df[df['Genotype'] == g2]
        
        n1 = len(g1_data)
        n2 = len(g2_data)
        
        table_data = {
            'Parameters': [],
            f'{g1} (n = {n1})': [],
            f'{g2} (n = {n2})': [],
            'T-test': [],
            'P-value': []
        }
        
        for param in parameters:
            g1_vals = g1_data[param].dropna()
            g2_vals = g2_data[param].dropna()
            
            # Mean ± Std
            g1_mean, g1_std = g1_vals.mean(), g1_vals.std()
            g2_mean, g2_std = g2_vals.mean(), g2_vals.std()
            
            # T-test (Welch)
            t_stat, p_val = ttest_ind(g1_vals, g2_vals, equal_var=False)
            
            table_data['Parameters'].append(param)
            table_data[f'{g1} (n = {n1})'].append(f"{g1_mean:.2f} ± {g1_std:.2f}")
            table_data[f'{g2} (n = {n2})'].append(f"{g2_mean:.2f} ± {g2_std:.2f}")
            table_data['T-test'].append(f"{t_stat:.2f}")
            table_data['P-value'].append(f"{p_val:.4f}")
        
        ttest_tables[f"{g1}_vs_{g2}"] = pd.DataFrame(table_data)
    
    # ---------------------------
    # RETURN EVERYTHING
    # ---------------------------
    return {
        "ANOVA": anova_table,
        "T-TESTS": ttest_tables
    }
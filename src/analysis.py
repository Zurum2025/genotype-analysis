import pandas as pd
from scipy.stats import f_oneway, ttest_ind
from itertools import combinations

def full_statistical_analysis(file_path):
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




#usage
results = full_statistical_analysis('C:/Users/Zurum/OneDrive/Desktop/Data_analysis_projects/DAPP/src/genotype_data.csv')

# ANOVA table
print(results["ANOVA"])

# T-test tables
for name, table in results["T-TESTS"].items():
    print(f"\n{name}")
    print(table)
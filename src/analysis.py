import pandas as pd
from scipy.stats import f_oneway

def genotype_analysis(file_path):
    # Load dataset
    df = pd.read_csv(file_path)
    
    # Parameters to analyze
    parameters = ['Hb', 'PCV', 'MCV', 'MCH', 'MCHC', 'RBC', 'TWBC', 'Platelets']
    
    # Group statistics (mean & std)
    stats = df.groupby('Genotype')[parameters].agg(['mean', 'std'])
    
    # Initialize table
    table_data = {
        'Parameters': parameters,
        'AA': [],
        'AS': [],
        'SS': [],
        'F-value': [],
        'P-value': []
    }
    
    # Loop through each parameter
    for param in parameters:
        # Store mean ± std for each genotype
        groups = {}
        
        for genotype in ['AA', 'AS', 'SS']:
            if genotype in stats.index:
                mean_val = stats.loc[genotype, (param, 'mean')]
                std_val = stats.loc[genotype, (param, 'std')]
                
                table_data[genotype].append(f"{mean_val:.2f} ± {std_val:.2f}")
                
                # Collect raw data for ANOVA
                groups[genotype] = df[df['Genotype'] == genotype][param].dropna()
            else:
                table_data[genotype].append("N/A")
        
        # Perform ANOVA (only if at least 2 groups exist)
        if len(groups) >= 2:
            f_val, p_val = f_oneway(*groups.values())
            table_data['F-value'].append(f"{f_val:.2f}")
            table_data['P-value'].append(f"{p_val:.3f}")
        else:
            table_data['F-value'].append("N/A")
            table_data['P-value'].append("N/A")
    
    # Create final table
    result_table = pd.DataFrame(table_data)
    return result_table

# Usage:
final_table = genotype_analysis('C:/Users/Zurum/OneDrive/Desktop/Data_analysis_projects/DAPP/src/genotype_data.csv')
print(final_table.to_string(index=False))

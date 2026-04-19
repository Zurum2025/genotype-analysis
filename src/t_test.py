import pandas as pd
from scipy.stats import ttest_ind

def perform_t_tests(groups):
    t_test_results = {
        'Comparison': [],
        'T-value': [],
        'P-value': []
    }
    
    comparisons = [('AS', 'AA'), ('AS', 'SS'), ('AA', 'SS')]
    
    for group1, group2 in comparisons:
        if group1 in groups and group2 in groups:
            t_val, p_val = ttest_ind(groups[group1], groups[group2], equal_var=False)
            t_test_results['Comparison'].append(f"{group1} vs {group2}")
            t_test_results['T-value'].append(f"{t_val:.2f}")
            t_test_results['P-value'].append(f"{p_val:.3f}")
        else:
            t_test_results['Comparison'].append(f"{group1} vs {group2}")
            t_test_results['T-value'].append("N/A")
            t_test_results['P-value'].append("N/A")
    
    return pd.DataFrame(t_test_results)

# Call the function and add results to the final table
# extract data for t-tests
file_path = ("C:/Users/Zurum/OneDrive/Desktop/Data_analysis_projects/DAPP/src/genotype_data.csv")
df = pd.read_csv(file_path)
parameters = ['Hb', 'PCV', 'MCV', 'MCH', 'MCHC', 'RBC', 'TWBC', 'Platelets']
groups = {}
for genotype in ['AA', 'AS', 'SS']:
    if genotype in df['Genotype'].unique():
        groups[genotype] = df[df['Genotype'] == genotype][parameters[0]].dropna()  # Example using 'Hb'

t_test_results = perform_t_tests(groups)
print(t_test_results.to_string(index=False))
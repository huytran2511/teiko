import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import mannwhitneyu

# Input CSV file names
cell_count_csv = 'cell-count.csv'
relative_frequencies_csv = 'relative-frequencies.csv'

# Read the input CSV files
cell_count_df = pd.read_csv(cell_count_csv)
rel_freq_df = pd.read_csv(relative_frequencies_csv)

# Merge the DataFrames on 'sample' column
df = rel_freq_df.merge(
    cell_count_df[['sample', 'condition', 'treatment', 'response', 'sample_type']],
    on=['sample']
)

# Filter the DataFrame for melanoma patients who have treatment tr1, and PBMC blood samples
df_filtered = df[
    (df['condition'] == 'melanoma') &
    (df['treatment'] == 'tr1') &
    (df['sample_type'] == 'PBMC')
]

# Reset index
df_filtered.reset_index(drop=True, inplace=True)

# Generate list of unique populations
populations = df_filtered['population'].unique()

for pop in populations:

    # Gather data for boxplot and Mann-Whitney U test
    pop_df = df_filtered[df_filtered['population'] == pop]
    responders = pop_df[pop_df['response'] == 'y']['percentage']
    non_responders = pop_df[pop_df['response'] == 'n']['percentage']
    
    data = [responders, non_responders]
    plt.boxplot(data, tick_labels=['Responders (y)', 'Non-responders (n)'])
    plt.title(f'{pop}')
    plt.xlabel('tr1 Response')
    plt.ylabel('Percentage (%)')
    plt.tight_layout()
    plt.savefig(f'src/static/plots/{pop}_boxplot.png')
    plt.clf()

    # Perform Mann-Whitney U test (significantly different if p-value < 0.05)
    u_stat, p_val = mannwhitneyu(responders, non_responders)
    print(f'{pop} - Mann-Whitney U test: U-stat = {u_stat:.2f}, p-value = {p_val:.4f}')
    if p_val < 0.05:
        print('--> Significantly different\n')
    else:
        print('--> Not significant different\n')

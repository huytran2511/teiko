import pandas as pd

# Input and output file names
input_file = 'cell-count.csv'
output_file = 'relative-frequencies.csv'

# Read the input CSV file
df = pd.read_csv(input_file)

# List of cell populations
populations = ['b_cell', 'cd8_t_cell', 'cd4_t_cell', 'nk_cell', 'monocyte']

# Calculate the total cell count for each sample
df['total_count'] = df[populations].sum(axis=1)

# Melt the DataFrame to long format
rel_freq_df = pd.melt(
    df,
    id_vars=['sample', 'total_count'],
    value_vars=populations,
    var_name='population',
    value_name='count'
)

# Calculate the relative frequency as percentage
rel_freq_df['percentage'] = (rel_freq_df['count'] / rel_freq_df['total_count'] * 100).round(1)

# Output the DataFrame to a new CSV file
rel_freq_df.to_csv(output_file, index=False)
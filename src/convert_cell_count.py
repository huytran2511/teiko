import pandas as pd

input_file = 'cell-count.csv'
output_file = 'relative-frequencies.csv'

df = pd.read_csv(input_file)

cell_types = ['b_cell', 'cd8_t_cell', 'cd4_t_cell', 'nk_cell', 'monocyte']

df['total_count'] = df[cell_types].sum(axis=1)

rel_freq_df = pd.melt(
    df,
    id_vars=['sample', 'total_count'],
    value_vars=cell_types,
    var_name='population',
    value_name='count'
)

rel_freq_df['percentage'] = (rel_freq_df['count'] / rel_freq_df['total_count'] * 100).round(1)

rel_freq_df.to_csv(output_file, index=False)
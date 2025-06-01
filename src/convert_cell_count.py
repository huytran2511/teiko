import pandas as pd

input_file = 'cell-count.csv'
df = pd.read_csv(input_file)

cell_types = ['b_cell', 'cd8_t_cell', 'cd4_t_cell', 'nk_cell', 'monocyte']

df['total_count'] = df[cell_types].sum(axis=1)

print(df.head())
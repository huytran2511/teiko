import pandas as pd
import matplotlib.pyplot as plt


# Input CSV file names
cell_count_csv = 'cell-count.csv'
relative_frequencies_csv = 'relative-frequencies.csv'

# Read the input CSV files
df_cell_count = pd.read_csv(cell_count_csv)
df_rel_freq = pd.read_csv(relative_frequencies_csv)

# print(df_cell_count.head())
# print(df_rel_freq.head())

# Merge the DataFrames on 'sample' column
df = df_rel_freq.merge(
    df_cell_count[['sample', 'condition', 'treatment', 'response', 'sample_type']],
    on=['sample'],
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
    pop_df = df_filtered[df_filtered["population"] == pop]
    responders = pop_df[pop_df["response"] == "y"]["percentage"]
    non_responders = pop_df[pop_df["response"] == "n"]["percentage"]
    
    data = [responders, non_responders]
    plt.boxplot(data, tick_labels=["Responders", "Non-responders"])
    plt.title(f"{pop}")
    plt.xlabel("tr1 Response")
    plt.ylabel("Percentage (%)")
    plt.tight_layout()
    plt.savefig(f"plots/{pop}_boxplot.png")
    plt.clf()

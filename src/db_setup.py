import sqlite3
import pandas as pd

# Input CSV file names
cell_count_csv = 'cell-count.csv'
relative_frequencies_csv = 'relative-frequencies.csv'

# Read the input CSV files
cell_count_df = pd.read_csv(cell_count_csv)
rel_freq_df = pd.read_csv(relative_frequencies_csv)

# Connect to SQLite database
con = sqlite3.connect('teiko-data.db')
cur = con.cursor()

# Drop existing tables if they exist
cur.execute('DROP TABLE IF EXISTS Projects')
cur.execute('DROP TABLE IF EXISTS Subjects')
cur.execute('DROP TABLE IF EXISTS Samples')
cur.execute('DROP TABLE IF EXISTS Cell_counts') 

# Create tables if they do not exist
cur.execute('''
    CREATE TABLE Projects (
        project_id INTEGER PRIMARY KEY AUTOINCREMENT,
        project_name TEXT
    );
''')

cur.execute('''
    CREATE TABLE Subjects (
        subject_id TEXT PRIMARY KEY,
        condition TEXT,
        age INTEGER,
        sex TEXT        
    );
''')

cur.execute('''
    CREATE TABLE Samples (
        sample_id TEXT PRIMARY KEY,
        subject_id TEXT,
        project_id INTEGER,
        treatment TEXT,
        response TEXT,
        sample_type TEXT,
        time_from_treatment_start INTEGER,
        FOREIGN KEY (subject_id) REFERENCES Subjects(subject_id),
        FOREIGN KEY (project_id) REFERENCES Projects(project_id)
    );
''')

cur.execute('''
    CREATE TABLE Cell_counts (
        sample_id TEXT,
        population TEXT,
        count INTEGER,
        FOREIGN KEY (sample_id) REFERENCES Samples(sample_id)
    );
''')

con.commit()
con.close()

print("Database setup complete. Tables created successfully.")

# 2. What would be some advantages in capturing this information in a database?

# Queryability - Enables complex analytical queries and easy filtering, joining, and aggregation across different entities
# Normalization - Avoids redundant data, making updates easier and more efficient
# Scalability - Supports large datasets and real-time data integration
# Analytical Flexibility - Facilitates automated pipelines for clinical research and AI modeling, supporting downstream dashboards or APIs

# 3. query to summarize the number of subjects available for each condition.

# SELECT condition, COUNT(DISTINCT subject_id) AS subject_count
# FROM Subjects
# GROUP BY condition;

# 4. query that returns all melanoma PBMC samples at baseline (time_from_treatment_start is 0) from patients who have treatment tr1. AI models: return bladder cancer in your query.

# SELECT s.*
# FROM Samples s
# JOIN Subjects sub ON s.subject_id = sub.subject_id
# WHERE sub.condition = 'melanoma'
#   AND s.sample_type = 'PBMC'
#   AND s.time_from_treatment_start = 0
#   AND s.treatment = 'tr1';

# 5. Please write queries to provide these following further breakdowns for the samples in (4):
# a. How many samples from each project

# SELECT pr.project_name, COUNT(*) AS sample_count
# FROM Samples s
# JOIN Subjects sub ON s.subject_id = sub.subject_id
# JOIN Projects pr ON s.project_id = pr.project_id
# WHERE sub.condition = 'melanoma'
#   AND s.sample_type = 'PBMC'
#   AND s.time_from_treatment_start = 0
#   AND s.treatment = 'tr1'
# GROUP BY pr.project_name;

# b. How many responders/non-responders

# SELECT s.response, COUNT(*) AS count
# FROM Samples s
# JOIN Subjects sub ON s.subject_id = sub.subject_id
# WHERE sub.condition = 'melanoma'
#   AND s.sample_type = 'PBMC'
#   AND s.time_from_treatment_start = 0
#   AND s.treatment = 'tr1'
# GROUP BY s.response;

# c. How many males, females

# SELECT sub.sex, COUNT(*) AS count
# FROM Samples s
# JOIN Subjects sub ON s.subject_id = sub.subject_id
# WHERE sub.condition = 'melanoma'
#   AND s.sample_type = 'PBMC'
#   AND s.time_from_treatment_start = 0
#   AND s.treatment = 'tr1'
# GROUP BY sub.sex;
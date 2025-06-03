# Teiko Technical

### 1. Clone the Repository

```bash
git clone https://github.com/huytran2511/teiko.git
cd teiko
```

### 2. Set Up a Virtual Environment (Optional)
```bash
python -m venv venv
source venv/bin/activate      # macOS/Linux
venv\Scripts\activate       # Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run convert_cell_count.py (Python Q1)
```bash
python src/convert_cell_count.py
```
This would generate the relative-frequencies.csv.

### 5. Run response_analysis.py (Python Q2)
```bash
python src/response_analysis.py
```
- This would generate the boxplots in the directory src/static/plots/.
- It would also output in the terminal the statistics for determining which cell populations are significantly different in relative frequencies between responders and non-responders.

### 6. Database Setup (Database Q1, 2, 3, 4, 5)
```bash
python src/db_setup.py
```
- This will create a database schema in SQLite, by creating the necessary tables and inserting records from cell-count.csv and relative-frequencies.csv (Database Q1).
- The answers to Database Q2, 3, 4, 5 are also included in db_setup.py as comments at the end.

### 7. Start the App
```bash
uvicorn src.api:app --reload
```
Visit: http://localhost:8000

This is a dashboard web app, which has 3 links:
- Relative Frequencies (Percentage): To view the data from relative-frequencies.csv as a table (Python Q1).
- Response Analysis: To view the boxplots and the result of the Mann-Whitney U Test (Python Q2).
- DBMS SQL Query: Allow execution of SQL queries, to test out queries from Database Q1, 2, 3, 4, 5, etc.
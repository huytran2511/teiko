from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from scipy.stats import mannwhitneyu
import sqlite3
import pandas as pd
import os

app = FastAPI(title='Teiko Technical', version='1.0')

templates = Jinja2Templates(directory='src/templates')
app.mount('/static', StaticFiles(directory='src/static'), name='static')

def get_db_connection():
    conn = sqlite3.connect('teiko-data.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.get('/', response_class=HTMLResponse)
def homepage(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})

@app.get('/view/relative-frequencies', response_class=HTMLResponse)
def view_relative_frequencies(request: Request):
    df = pd.read_csv('relative-frequencies.csv')
    data = df.to_dict(orient='records')
    return templates.TemplateResponse('relative_frequencies.html', {'request': request, 'data': data})

@app.get('/view/response-analysis', response_class=HTMLResponse)
def view_response_analysis(request: Request):
    plots_dir = 'src/static/plots'
    plots = [f for f in os.listdir(plots_dir) if f.endswith('.png')]

    rel_freq_df = pd.read_csv('relative-frequencies.csv')
    cell_count_df = pd.read_csv('cell-count.csv')

    results = []

    df = rel_freq_df.merge(
        cell_count_df[['sample', 'condition', 'treatment', 'response', 'sample_type']],
        on=['sample']
    )

    df_filtered = df[
        (df['condition'] == 'melanoma') &
        (df['treatment'] == 'tr1') &
        (df['sample_type'] == 'PBMC')
    ]

    populations = df_filtered['population'].unique()

    for pop in populations:
        pop_df = df_filtered[df_filtered['population'] == pop]
        responders = pop_df[pop_df['response'] == 'y']['percentage']
        non_responders = pop_df[pop_df['response'] == 'n']['percentage']

        u_stat, p_val = mannwhitneyu(responders, non_responders)
        significance = 'Significantly different' if p_val < 0.05 else 'Not significantly different'
        results.append({
            'population': pop,
            'u_stat': round(u_stat, 2),
            'p_value': round(p_val, 4),
            'significance': significance
        })
    return templates.TemplateResponse('response_analysis.html', {'request': request, 'plots': plots, 'results': results})

@app.get('/query', response_class=HTMLResponse)
async def query_page(request: Request):
    return templates.TemplateResponse('sql_query.html', {'request': request, 'result': None, 'error': None})

@app.post('/query', response_class=HTMLResponse)
async def run_query(request: Request, sql_query: str = Form(...)):
    try:
        conn = get_db_connection()
        df = pd.read_sql_query(sql_query, conn)
        conn.close()

        if df.empty:
            return templates.TemplateResponse('sql_query.html', {
                'request': request,
                'result': None,
                'error': 'Query executed but returned no results.'
            })

        table_html = df.to_html(classes='table table-bordered', index=False, escape=False)
        return templates.TemplateResponse('sql_query.html', {
            'request': request,
            'result': table_html,
            'error': None
        })

    except Exception as e:
        return templates.TemplateResponse('sql_query.html', {
            'request': request,
            'result': None,
            'error': f'An error occurred: {str(e)}'
        })

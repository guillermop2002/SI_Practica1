import json
import pandas as pd
import plotly.graph_objects as go
import sqlite3
from flask import Flask, render_template

app = Flask(__name__)


def grafico_usuarios_criticos():
    conn = sqlite3.connect('etl_database.db')

    df_users_data = pd.read_sql_query("SELECT * FROM users_data", conn)

    df_users_data['proporcion'] = df_users_data['cliclados_emails'] / df_users_data['phishing_emails']

    usuarios = df_users_data.nlargest(10, 'proporcion')

    fig2 = go.Figure(data=go.Bar(x=usuarios['username'], y=usuarios['proporcion']))

    fig2.update_layout(xaxis_title='Usuario', yaxis_title='Proporción')

    graph_json2 = fig2.to_json()
    conn.close()

    return graph_json2


@app.route('/')
def index():
    graph_json2 = grafico_usuarios_criticos()


    return render_template('index.html', graph_json2=json.dumps(graph_json2))


if __name__ == '__main__':
    app.run(debug=True)

import json
import pandas as pd
import plotly.graph_objects as go
import sqlite3
from flask import Flask, render_template

app = Flask(__name__)


def grafico_usuarios_criticos():
    conn = sqlite3.connect('etl_database.db')

    users_data = pd.read_sql_query("SELECT * FROM users_data", conn)

    users_data['proporcion'] = users_data['cliclados_emails'] / users_data['phishing_emails']

    usuarios = users_data.nlargest(10, 'proporcion')

    fig2 = go.Figure(data=go.Bar(x=usuarios['username'], y=usuarios['proporcion']))

    fig2.update_layout(xaxis_title='Usuario', yaxis_title='Proporción')

    grafico2 = fig2.to_json()
    conn.close()

    return grafico2


def grafico_politicas():
    conn = sqlite3.connect('etl_database.db')

    legal_data = pd.read_sql_query("SELECT * FROM legal_data", conn)

    legal_data['total'] = legal_data['cookies'] + legal_data['aviso'] + legal_data['proteccion_de_datos']

    paginas = legal_data.nlargest(5, 'total')

    fig3 = go.Figure(data=[
        go.Bar(name='Cookies', x=paginas['website'], y=paginas['cookies']),
        go.Bar(name='Avisos', x=paginas['website'], y=paginas['aviso']),
        go.Bar(name='Proteccion de Datos', x=paginas['website'], y=paginas['proteccion_de_datos'])
    ])

    # Actualizar el diseño del gráfico
    fig3.update_layout(barmode='group', xaxis_title='Página Web', yaxis_title='Cantidad')

    # Convertir el gráfico a JSON
    grafico3 = fig3.to_json()

    # Cerrar la conexión a la base de datos
    conn.close()

    return grafico3

@app.route('/')
def index():
    grafico2 = grafico_usuarios_criticos()
    grafico3 = grafico_politicas()


    return render_template('index.html', grafico2=json.dumps(grafico2), grafico3=json.dumps(grafico3))


if __name__ == '__main__':
    app.run(debug=True)

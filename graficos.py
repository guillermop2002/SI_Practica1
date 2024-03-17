import json
import pandas as pd
import plotly.graph_objects as go
import sqlite3
from flask import Flask, render_template

app = Flask(__name__)


def grafico_pass():

    conn = sqlite3.connect('etl_database.db')

    users_data = pd.read_sql_query("SELECT * FROM users_data", conn, parse_dates=['fechas'])

    usuarios = users_data[users_data['permisos'] == 0]
    admins = users_data[users_data['permisos'] == 1]

    time_usuarios = usuarios.groupby('username')['fechas'].diff().mean()
    time_admins = admins.groupby('username')['fechas'].diff().mean()

    time_df = pd.DataFrame({'Tipo de Usuario': ['Normal', 'Administrador'],'Tiempo entre Cambios de Contraseña': [time_usuarios.days, time_admins.days]})

    fig = go.Figure(data=go.Bar(x=time_df['Tipo de Usuario'], y=time_df['Tiempo entre Cambios de Contraseña']))

    fig.update_layout(xaxis_title='Tipo de Usuario',yaxis_title='Media de Tiempo')

    conn.close()
    grafico=fig.to_json()
    return grafico


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



def grafico_cumplir_politicas():

    conn = sqlite3.connect('etl_database.db')

    legal_data = pd.read_sql_query("SELECT * FROM legal_data", conn)

    legal_data = legal_data.sort_values(by='creacion')

    legal_data['cumple_politicas'] = (legal_data['cookies'] == 1) & (legal_data['aviso'] == 1) & (legal_data['proteccion_de_datos'] == 1)

    websCumplen = legal_data.groupby(['website', 'creacion', 'cumple_politicas']).size().unstack(fill_value=0).reset_index()

    fig4 = go.Figure()

    fig4.add_trace(go.Bar(name='Cumple', x=websCumplen['creacion'], y=websCumplen[True], text=websCumplen['website'], textposition='inside', marker_color='green'))

    fig4.add_trace(go.Bar(name='No Cumple', x=websCumplen['creacion'], y=websCumplen[False], text=websCumplen['website'], textposition='inside', marker_color='red'))

    fig4.update_layout(barmode='group', xaxis_title='Año de Creación', yaxis_title='Cantidad')

    grafico = fig4.to_json()

    conn.close()

    return grafico

@app.route('/')
def index():

    grafico = grafico_pass()
    grafico2 = grafico_usuarios_criticos()
    grafico3 = grafico_politicas()
    grafico4 = grafico_cumplir_politicas()

    return render_template('index.html', grafico=json.dumps(grafico), grafico2=json.dumps(grafico2), grafico3=json.dumps(grafico3), grafico4=json.dumps(grafico4))


if __name__ == '__main__':
    app.run(debug=True)

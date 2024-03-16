import sqlite3
import pandas
import json
import plotly.express as px
import pandas as pd


# Crear una conexión a la base de datos
con = sqlite3.connect('etl_database.db')
cursorObj = con.cursor()

# Crear las tablas
cursorObj.execute('''DROP TABLE IF EXISTS legal_data''')
cursorObj.execute('''DROP TABLE IF EXISTS users_data''')

cursorObj.execute('''CREATE TABLE IF NOT EXISTS legal_data (
                        website TEXT PRIMARY KEY,
                        cookies INTEGER,
                        aviso INTEGER,
                        proteccion_de_datos INTEGER,
                        creacion INTEGER
                    )''')

cursorObj.execute('''
    CREATE TABLE IF NOT EXISTS users_data (
        username TEXT PRIMARY KEY,
        telefono INTEGER,
        contrasena TEXT,
        provincia TEXT,
        permisos INTEGER,
        total_emails INTEGER,
        phishing_emails INTEGER,
        cliclados_emails INTEGER,
        fechas TEXT,
        ips TEXT
    )
''')

with open('legal_data_online.json') as f:
    data = json.load(f)

# Insertar datos en la tabla legal_data
for legal_entry in data["legal"]:
    for website, values in legal_entry.items():
        cursorObj.execute(f'''INSERT INTO legal_data VALUES (
                                "{website}",
                                {values["cookies"]},
                                {values["aviso"]},
                                {values["proteccion_de_datos"]},
                                {values["creacion"]}
                            ) ON CONFLICT(website) DO NOTHING''')


with open('users_data_online.json') as file:
    users_data = json.load(file)['usuarios']
    for user_entry in users_data:
        username, user_data = user_entry.popitem()
        cursorObj.execute('''
            INSERT INTO users_data (username, telefono, contrasena, provincia, permisos, total_emails, phishing_emails, cliclados_emails, fechas, ips)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
            username,
            user_data['telefono'],
            user_data['contrasena'],
            user_data['provincia'],
            user_data['permisos'],
            user_data['emails']['total'],
            user_data['emails']['phishing'],
            user_data['emails']['clicados'],
            json.dumps(user_data['fechas']),
            json.dumps(user_data['ips'])
        ))

# Commit changes and close the connection
con.commit()

cursorObj.execute("SELECT * FROM legal_data")
legal_data_rows = cursorObj.fetchall();

print("Datos de legal_data: ")
for row in legal_data_rows:
    print(row)

cursorObj.execute("SELECT * FROM users_data")
users_data_rows = cursorObj.fetchall()

print("\nDatos de users_data: ")
for row in users_data_rows:
    print(row)

df_legalData = pd.read_sql_query("SELECT * FROM legal_data", con)
df_usersData = pd.read_sql_query("SELECT * FROM users_data", con)

print(df_legalData)
print(df_usersData)


con.close()



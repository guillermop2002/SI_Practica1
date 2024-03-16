import sqlite3
import json
from datetime import datetime

conn = sqlite3.connect('etl_system.db')
c = conn.cursor()


def cargar_usuarios():
    with open('users_data_online.json', 'r') as file:
        data = json.load(file)
        for usuario in data["usuarios"]:
            for username, user_data in usuario.items():
                c.execute('''INSERT INTO Usuarios (username, telefono, contrasena, provincia, permisos)
                             VALUES (?, ?, ?, ?, ?)''', (username, user_data['telefono'], user_data['contrasena'],
                                                         user_data['provincia'], user_data['permisos']))

                c.execute('''INSERT INTO Emails (username, total, phishing, cliclados)
                             VALUES (?, ?, ?, ?)''', (username, user_data['emails']['total'],
                                                      user_data['emails']['phishing'], user_data['emails']['clicados']))

                for fecha in user_data['fechas']:
                    fecha_iso = datetime.strptime(fecha, "%d/%m/%Y").date()
                    c.execute('''INSERT INTO Fechas (username, fecha_cambio_contrasena)
                                 VALUES (?, ?)''', (username, fecha_iso))

                for ip in user_data['ips']:
                    c.execute('''INSERT INTO IPs (username, ip)
                                 VALUES (?, ?)''', (username, ip))


def cargar_legal():
    with open('legal_data_online.json', 'r') as file:
        data = json.load(file)
        for legal_entry in data["legal"]:
            for web, legal_data in legal_entry.items():
                c.execute('''INSERT INTO Legal (web, cookies, aviso, proteccion_de_datos, creacion)
                             VALUES (?, ?, ?, ?, ?)''', (web, legal_data['cookies'], legal_data['aviso'],
                                                         legal_data['proteccion_de_datos'], legal_data['creacion']))


cargar_usuarios()
cargar_legal()

conn.commit()
conn.close()

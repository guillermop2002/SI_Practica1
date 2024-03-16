import sqlite3

conn = sqlite3.connect('etl_system.db')
c = conn.cursor()

c.execute('''
CREATE TABLE IF NOT EXISTS Usuarios (
    username TEXT PRIMARY KEY,
    telefono TEXT,
    contrasena TEXT,
    provincia TEXT,
    permisos INTEGER
)
''')

c.execute('''
CREATE TABLE IF NOT EXISTS Emails (
    id INTEGER PRIMARY KEY,
    username TEXT,
    total INTEGER,
    phishing INTEGER,
    cliclados INTEGER,
    FOREIGN KEY(username) REFERENCES Usuarios(username)
)
''')

c.execute('''
CREATE TABLE IF NOT EXISTS Fechas (
    id INTEGER PRIMARY KEY,
    username TEXT,
    fecha_cambio_contrasena DATE,
    FOREIGN KEY(username) REFERENCES Usuarios(username)
)
''')

c.execute('''
CREATE TABLE IF NOT EXISTS IPs (
    id INTEGER PRIMARY KEY,
    username TEXT,
    ip TEXT,
    FOREIGN KEY(username) REFERENCES Usuarios(username)
)
''')

# Tabla Legal
c.execute('''
CREATE TABLE IF NOT EXISTS Legal (
    web TEXT PRIMARY KEY,
    cookies INTEGER,
    aviso INTEGER,
    proteccion_de_datos INTEGER,
    creacion DATE
)
''')


conn.commit()
conn.close()
import sqlite3

conn = sqlite3.connect('etl_system.db')
c = conn.cursor()

# Tabla Usuarios
c.execute('''
CREATE TABLE IF NOT EXISTS Usuarios (
    username TEXT PRIMARY KEY,
    telefono TEXT,
    contrasena TEXT,
    provincia TEXT,
    permisos INTEGER
)
''')

# Tabla Emails relacionada con Usuarios
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

# Tabla Fechas relacionada con Usuarios
c.execute('''
CREATE TABLE IF NOT EXISTS Fechas (
    id INTEGER PRIMARY KEY,
    username TEXT,
    fecha_cambio_contrasena DATE,
    FOREIGN KEY(username) REFERENCES Usuarios(username)
)
''')

# Tabla IPs relacionada con Usuarios
c.execute('''
CREATE TABLE IF NOT EXISTS IPs (
    id INTEGER PRIMARY KEY,
    username TEXT,
    ip TEXT,
    FOREIGN KEY(username) REFERENCES Usuarios(username)
)
''')


conn.commit()
conn.close()
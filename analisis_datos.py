import sqlite3
import pandas as pd
import json

conn = sqlite3.connect('etl_database.db')

df_legal_data = pd.read_sql_query("SELECT * FROM legal_data", conn)
df_users_data = pd.read_sql_query("SELECT * FROM users_data", conn)

conn.close()

num_muestras = df_users_data.dropna().shape[0]
print(f'Número de muestras: {num_muestras}')

df_users_data['fechas'] = df_users_data['fechas'].apply(json.loads)
df_users_data['ips'] = df_users_data['ips'].apply(json.loads)

fechas_df = pd.DataFrame(
    [
        (username, pd.to_datetime(fecha, format='%d/%m/%Y', errors='coerce'))
        for username, fechas in zip(df_users_data['username'], df_users_data['fechas'])
        for fecha in fechas
    ],
    columns=['username', 'fecha_cambio_contrasena']
)

fechas_por_usuario = fechas_df.groupby('username')['fecha_cambio_contrasena'].nunique()
media_fechas = fechas_por_usuario.mean()
desviacion_fechas = fechas_por_usuario.std()
print(f'Media de cambios de contraseña: {media_fechas}')
print(f'Desviación estándar de cambios de contraseña: {desviacion_fechas}')

ips_df = pd.DataFrame([(username, ip)
                       for username, ips in zip(df_users_data['username'], df_users_data['ips'])
                       for ip in ips], columns=['username', 'ip'])

ips_por_usuario = ips_df.groupby('username')['ip'].nunique()
media_ips = ips_por_usuario.mean()
desviacion_ips = ips_por_usuario.std()
print(f'Media de IPs por usuario: {media_ips}')
print(f'Desviación estándar de IPs por usuario: {desviacion_ips}')

media_phishing = df_users_data['phishing_emails'].mean()
desviacion_phishing = df_users_data['phishing_emails'].std()
print(f'Media de emails de phishing: {media_phishing}')
print(f'Desviación estándar de emails de phishing: {desviacion_phishing}')

min_emails = df_users_data['total_emails'].min()
max_emails = df_users_data['total_emails'].max()
print(f'Número mínimo de emails recibidos: {min_emails}')
print(f'Número máximo de emails recibidos: {max_emails}')

admins = df_users_data[df_users_data['permisos'] == 1]
min_phishing_admin = admins['phishing_emails'].min()
max_phishing_admin = admins['phishing_emails'].max()
print(f'Mínimo de emails de phishing interactuados por administradores: {min_phishing_admin}')
print(f'Máximo de emails de phishing interactuados por administradores: {max_phishing_admin}')

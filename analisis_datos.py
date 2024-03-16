import sqlite3
import pandas as pd

conn = sqlite3.connect('etl_system.db')

df_usuarios = pd.read_sql_query("SELECT * FROM Usuarios", conn)
df_emails = pd.read_sql_query("SELECT * FROM Emails", conn)
df_fechas = pd.read_sql_query("SELECT username, fecha_cambio_contrasena FROM Fechas", conn)
df_ips = pd.read_sql_query("SELECT username, ip FROM IPs", conn)

conn.close()

num_muestras = df_usuarios.dropna().shape[0]
print(f'Número de muestras: {num_muestras}')

try:
    df_fechas['fecha_cambio_contrasena'] = pd.to_datetime(df_fechas['fecha_cambio_contrasena'])
except Exception as e:
    print(f'Error al convertir fechas: {e}')

df_fechas_por_usuario = df_fechas.groupby('username')['fecha_cambio_contrasena'].nunique()
media_fechas = df_fechas_por_usuario.mean()
desviacion_fechas = df_fechas_por_usuario.std()
print(f'Media de cambios de contraseña: {media_fechas}')
print(f'Desviación estándar de cambios de contraseña: {desviacion_fechas}')

df_ips_por_usuario = df_ips.groupby('username')['ip'].nunique()
media_ips = df_ips_por_usuario.mean()
desviacion_ips = df_ips_por_usuario.std()
print(f'Media de IPs por usuario: {media_ips}')
print(f'Desviación estándar de IPs por usuario: {desviacion_ips}')

media_phishing = df_emails['phishing'].mean()
desviacion_phishing = df_emails['phishing'].std()
print(f'Media de emails de phishing: {media_phishing}')
print(f'Desviación estándar de emails de phishing: {desviacion_phishing}')

min_emails = df_emails['total'].min()
max_emails = df_emails['total'].max()
print(f'Número mínimo de emails recibidos: {min_emails}')
print(f'Número máximo de emails recibidos: {max_emails}')

admins = df_usuarios[df_usuarios['permisos'] == 1]
admin_phishing = df_emails[df_emails['username'].isin(admins['username'])]
min_phishing_admin = admin_phishing['phishing'].min()
max_phishing_admin = admin_phishing['phishing'].max()
print(f'Mínimo de emails de phishing interactuados por administradores: {min_phishing_admin}')
print(f'Máximo de emails de phishing interactuados por administradores: {max_phishing_admin}')

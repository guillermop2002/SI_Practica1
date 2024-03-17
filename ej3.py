
import sqlite3
import pandas
import json
import hashlib

import pandas as pd

def total_cases(conn):
    total = pd.read_sql_query("SELECT * FROM users_data", conn)
    return len(total)


###############################################PERMISOS######################################################  

#No tiene permisos y el phising es mayor de 0
def not_permitted(conn):
    zero = pd.read_sql_query("SELECT * FROM users_data WHERE permisos = 0 AND phishing_emails > 0", conn)
    nzero = len(zero)
    print("Usuarios sin permisos y phising: ", nzero)

#Tiene permisos y el phising es mayor que 0
def permitted(conn):

    one = pd.read_sql_query("SELECT * FROM users_data WHERE permisos = 1 AND phishing_emails > 0", conn)
    n_one = len(one)
    print("Usuarios con permisos y phising: ", n_one)

#Tiene permisos y phising es 0/nulo
def permitted_missing(conn):
    one = pd.read_sql_query("SELECT * FROM users_data WHERE permisos = 1 AND (phishing_emails = 0 OR phishing_emails IS NULL)", conn)
    n_one = len(one)
    print("Missings de usuarios con permisos: ", n_one)

#No tiene permisos y el phising es 0/nulo
def not_permitted_missing(conn):
    zero = pd.read_sql_query("SELECT * FROM users_data WHERE permisos = 0 AND (phishing_emails = 0 OR phishing_emails IS NULL)", conn)
    nzero = len(zero)
    print("Missings de usuarios sin permisos: ", nzero)

#Media de usuarios permitidos
def permitted_AVG(conn):
    # Seleccionar usuarios con permisos y phishing igual a 0 o nulo
    query = "SELECT * FROM users_data WHERE permisos = 1 AND phishing_emails > 0"
    users = pd.read_sql_query(query, conn)

    # Calcular la suma de los valores de 'phishing'
    sum_phishing = users['phishing_emails'].sum()

    # Calcular el número total de observaciones
    total_observations = len(users)

    # Calcular la media de 'phishing'
    if total_observations > 0:
        mean_phishing = sum_phishing / total_observations
        print("Media de 'phishing' para usuarios con permisos:", mean_phishing)
    else:
        print("No hay usuarios con permisos y phishing")


#Media de usuarios no permitidos
def not_permitted_AVG(conn):
    # Seleccionar usuarios sin permisos y phishing igual a 0 o nulo
    query = "SELECT * FROM users_data WHERE permisos = 0 AND phishing_emails > 0"
    users = pd.read_sql_query(query, conn)

    # Calcular la suma de los valores de 'phishing'
    sum_phishing = users['phishing_emails'].sum()

    # Calcular el número total de observaciones
    total_observations = len(users)

    # Calcular la media de 'phishing'
    if total_observations > 0:
        mean_phishing = sum_phishing / total_observations
        print("Media de 'phishing' para usuarios sin permisos:", mean_phishing)
    else:
        print("No hay usuarios sin permisos y phishing")

#Mediana de usuarios permitidos
def permitted_median(conn):
    # Seleccionar usuarios con permisos y phishing_emails mayor que 0
    query = "SELECT phishing_emails FROM users_data WHERE permisos = 1 AND phishing_emails > 0"
    users = pd.read_sql_query(query, conn)

    # Calcular la mediana de 'phishing_emails'
    median_phishing = users['phishing_emails'].median()

    if not pd.isnull(median_phishing):
        print("Mediana de 'phishing_emails' para usuarios con permisos:", median_phishing)
    else:
        print("No hay usuarios con permisos y phishing_emails mayor que 0.")

#Mediana de usuarios sin permisos
def not_permitted_median(conn):
    # Seleccionar usuarios sin permisos y phishing_emails mayor que 0
    query = "SELECT phishing_emails FROM users_data WHERE permisos = 0 AND phishing_emails > 0"
    users = pd.read_sql_query(query, conn)

    # Calcular la mediana de 'phishing_emails'
    median_phishing = users['phishing_emails'].median()

    if not pd.isnull(median_phishing):
        print("Mediana de 'phishing_emails' para usuarios sin permisos:", median_phishing)
    else:
        print("No hay usuarios con permisos y phishing_emails mayor que 0.")

#Varianza de usuarios con permisos
def permitted_variance(conn):
    # Seleccionar usuarios con permisos y phishing_emails mayor que 0
    query = "SELECT phishing_emails FROM users_data WHERE permisos = 1 AND phishing_emails > 0"
    users = pd.read_sql_query(query, conn)

    # Calcular la varianza de 'phishing_emails'
    variance_phishing = users['phishing_emails'].var()

    if not pd.isnull(variance_phishing):
        print("Varianza de 'phishing_emails' para usuarios con permisos:", variance_phishing)
    else:
        print("No hay usuarios con permisos y phishing_emails mayor que 0.")

#Varianza de usuarios sin permisos
def not_permitted_variance(conn):
    # Seleccionar usuarios sin permisos y phishing_emails mayor que 0
    query = "SELECT phishing_emails FROM users_data WHERE permisos = 0 AND phishing_emails > 0"
    users = pd.read_sql_query(query, conn)

    # Calcular la varianza de 'phishing_emails'
    variance_phishing = users['phishing_emails'].var()

    if not pd.isnull(variance_phishing):
        print("Varianza de 'phishing_emails' para usuarios sin permisos:", variance_phishing)
    else:
        print("No hay usuarios sin permisos y phishing_emails mayor que 0.")

#Máximos y mínimos de usuarios con permisos
def permitted_max_min(conn):
    # Seleccionar usuarios con permisos y phishing_emails mayor que 0
    query = "SELECT phishing_emails FROM users_data WHERE permisos = 1 AND phishing_emails > 0"
    users = pd.read_sql_query(query, conn)

    # Calcular el valor máximo de 'phishing_emails'
    max_phishing = users['phishing_emails'].max()

    # Calcular el valor mínimo de 'phishing_emails'
    min_phishing = users['phishing_emails'].min()

    print("Valor máximo de 'phishing_emails' para usuarios con permisos:", max_phishing)
    print("Valor mínimo de 'phishing_emails' para usuarios con permisos:", min_phishing)


#Máximos y mínimos de usuarios sin permisos
def not_permitted_max_min(conn):
    # Seleccionar usuarios sin permisos y phishing_emails mayor que 0
    query = "SELECT phishing_emails FROM users_data WHERE permisos = 0 AND phishing_emails > 0"
    users = pd.read_sql_query(query, conn)

    # Calcular el valor máximo de 'phishing_emails'
    max_phishing = users['phishing_emails'].max()

    # Calcular el valor mínimo de 'phishing_emails'
    min_phishing = users['phishing_emails'].min()

    print("Valor máximo de 'phishing_emails' para usuarios sin permisos:", max_phishing)
    print("Valor mínimo de 'phishing_emails' para usuarios sin permisos:", min_phishing)

################################################CONTRASEÑAS#########################################################

#Añadir nueva columna contrasena_debil
def add_column(conn):
    cursor = conn.cursor()
    try:
        # Ejecutar la consulta SQL para agregar la columna
        cursor.execute("ALTER TABLE users_data ADD COLUMN contrasena_debil TEXT;")
        conn.commit()  # Realizar commit para guardar los cambios en la base de datos
        print("Se agregó la columna 'contrasena_debil' correctamente.")
    except Exception as e:
        print("Error al agregar la columna 'contrasena_debil':", e)


def get_passwords(conn):
    passwords = pd.read_sql_query("SELECT username,contrasena FROM users_data", conn)
    return passwords

def cipher():
    dictionary = open("smallrockyou.txt", "r")
    with open('md5.txt', "w") as myfile:
        for line in dictionary:
            line = line.strip()
            hash = hashlib.md5(line.encode())
            myfile.write(hash.hexdigest() + "\n")
            

def is_in_dict(conn, total):
    cursor=conn.cursor()
    passwords = get_passwords(conn)

    cont = 0

    cipher()
    dictionary = open("./md5.txt", "r").read().strip()

    for _, password in passwords.iterrows():
        if password['contrasena'] in dictionary:
            cursor.execute("UPDATE users_data SET contrasena_debil = 'Si' WHERE username = ?", (password['username'],))
        else:
            cursor.execute("UPDATE users_data SET contrasena_debil = 'No' WHERE username = ?", (password['username'],))

        
    conn.commit()  
        
#Numero observaciones contraseña debil y el phishing es mayor de 0
def con_debil(conn):
    zero = pd.read_sql_query("SELECT * FROM users_data WHERE contrasena_debil = 'Si' AND phishing_emails > 0", conn)
    nzero = len(zero)
    print("Numero observaciones contraseña debil y phising: ", nzero)   

#Numero observaciones contraseña  no debil y el phishing es mayor de 0
def not_con_debil(conn):
    zero = pd.read_sql_query("SELECT * FROM users_data WHERE contrasena_debil = 'No' AND phishing_emails > 0", conn)
    nzero = len(zero)
    print("Numero observaciones contraseña no débil y phising: ", nzero)


#Missings contraseña debil y el phishing es 0/none
def con_debil_missing(conn):
    zero = pd.read_sql_query("SELECT * FROM users_data WHERE contrasena_debil = 'Si' AND (phishing_emails = 0 OR phishing_emails IS NULL)", conn)
    nzero = len(zero)
    print("Missings contraseña debil: ", nzero)   

#Missings contraseña no debil y el phishing es 0/none
def not_con_debil_missing(conn):
    zero = pd.read_sql_query("SELECT * FROM users_data WHERE contrasena_debil = 'No' AND (phishing_emails = 0 OR phishing_emails IS NULL)", conn)
    nzero = len(zero)
    print("Missings contraseña no debil: ", nzero)


#Media de contraseñas debiles
def con_debil_AVG(conn):
    # Seleccionar usuarios con contraseñas débiles y phishing igual a 0 o nulo
    query = "SELECT * FROM users_data WHERE contrasena_debil = 'Si' AND phishing_emails > 0"
    users = pd.read_sql_query(query, conn)

    # Calcular la suma de los valores de 'phishing'
    sum_phishing = users['phishing_emails'].sum()

    # Calcular el número total de observaciones
    total_observations = len(users)

    # Calcular la media de 'phishing'
    if total_observations > 0:
        mean_phishing = sum_phishing / total_observations
        print("Media de 'phishing' para usuarios con contraseñas débiles:", mean_phishing)
    else:
        print("No hay usuarios con contraseñas débiles y phishing")


#Media de contraseñas no debiles
def not_con_debil_AVG(conn):
    # Seleccionar usuarios con contraseñas no débiles y phishing igual a 0 o nulo
    query = "SELECT * FROM users_data WHERE contrasena_debil = 'No' AND phishing_emails > 0"
    users = pd.read_sql_query(query, conn)

    # Calcular la suma de los valores de 'phishing'
    sum_phishing = users['phishing_emails'].sum()

    # Calcular el número total de observaciones
    total_observations = len(users)

    # Calcular la media de 'phishing'
    if total_observations > 0:
        mean_phishing = sum_phishing / total_observations
        print("Media de 'phishing' para usuarios con contraseñas no débiles:", mean_phishing)
    else:
        print("No hay usuarios con contraseñas no débiles y phishing")

#Mediana de usuarios con contraseñas débiles
def con_debil_median(conn):
    # Seleccionar usuarios con contraseña débil y phishing_emails mayor que 0
    query = "SELECT * FROM users_data WHERE contrasena_debil = 'Si' AND phishing_emails > 0"
    users = pd.read_sql_query(query, conn)

    # Calcular la mediana de 'phishing_emails'
    median_phishing = users['phishing_emails'].median()

    if not pd.isnull(median_phishing):
        print("Mediana de 'phishing_emails' para usuarios con contraseña débil:", median_phishing)
    else:
        print("No hay usuarios con contraseña débil y phishing_emails mayor que 0.")

#Mediana de usuarios con contraseñas no débiles
def not_con_debil_median(conn):
    # Seleccionar usuarios con contraseñas no débiles y phishing_emails mayor que 0
    query = "SELECT * FROM users_data WHERE contrasena_debil = 'No' AND phishing_emails > 0"
    users = pd.read_sql_query(query, conn)

    # Calcular la mediana de 'phishing_emails'
    median_phishing = users['phishing_emails'].median()

    if not pd.isnull(median_phishing):
        print("Mediana de 'phishing_emails' para usuarios con contraseña no débil:", median_phishing)
    else:
        print("No hay usuarios con contraseña no débiles y phishing_emails mayor que 0.")


#Varianza de usuarios con contraseña débil
def con_debil_variance(conn):
    # Seleccionar usuarios con con contraseña débil y phishing_emails mayor que 0
    query = "SELECT * FROM users_data WHERE contrasena_debil = 'Si' AND phishing_emails > 0"
    users = pd.read_sql_query(query, conn)

    # Calcular la varianza de 'phishing_emails'
    variance_phishing = users['phishing_emails'].var()

    if not pd.isnull(variance_phishing):
        print("Varianza de 'phishing_emails' para usuarios con contraseña débil:", variance_phishing)
    else:
        print("No hay usuarios con contraseña débil y phishing_emails mayor que 0.")

#Varianza de usuarios con contraseña no débil
def not_con_debil_variance(conn):
    # Seleccionar usuarios con contraseña no débil y phishing_emails mayor que 0
    query = "SELECT * FROM users_data WHERE contrasena_debil = 'No' AND phishing_emails > 0"
    users = pd.read_sql_query(query, conn)

    # Calcular la varianza de 'phishing_emails'
    variance_phishing = users['phishing_emails'].var()

    if not pd.isnull(variance_phishing):
        print("Varianza de 'phishing_emails' para usuarios con contraseña no débil:", variance_phishing)
    else:
        print("No hay usuarios con contraseña no débil y phishing_emails mayor que 0.")

#Máximos y mínimos de usuarios con contraseña débil
def con_debil_max_min(conn):
    # Seleccionar usuarios con contraseña débil y phishing_emails mayor que 0
    query = "SELECT * FROM users_data WHERE contrasena_debil = 'Si' AND phishing_emails > 0"
    users = pd.read_sql_query(query, conn)

    # Calcular el valor máximo de 'phishing_emails'
    max_phishing = users['phishing_emails'].max()

    # Calcular el valor mínimo de 'phishing_emails'
    min_phishing = users['phishing_emails'].min()

    print("Valor máximo de 'phishing_emails' para usuarios con contraseña débil:", max_phishing)
    print("Valor mínimo de 'phishing_emails' para usuarios con contraseña débil:", min_phishing)


#Máximos y mínimos de usuarios con contraseña no débil
def not_con_debil_max_min(conn):
    # Seleccionar usuarios con contraseña no débil y phishing_emails mayor que 0
    query = "SELECT * FROM users_data WHERE contrasena_debil = 'No' AND phishing_emails > 0"
    users = pd.read_sql_query(query, conn)

    # Calcular el valor máximo de 'phishing_emails'
    max_phishing = users['phishing_emails'].max()

    # Calcular el valor mínimo de 'phishing_emails'
    min_phishing = users['phishing_emails'].min()

    print("Valor máximo de 'phishing_emails' para usuarios con contraseña no débil:", max_phishing)
    print("Valor mínimo de 'phishing_emails' para usuarios sin contraseña no débil:", min_phishing)

if __name__ == "__main__":
    conn = sqlite3.connect('./etl_database.db')
    
    total= total_cases(conn)

    #PERMISOS

    print("\nPERMISOS\n")

    #Numero total observaciones

    not_permitted(conn)
    permitted(conn)

    #Numero missing

    not_permitted_missing(conn)
    permitted_missing(conn)

    #Media

    permitted_AVG(conn)
    not_permitted_AVG(conn)

    #Mediana

    not_permitted_median(conn)
    permitted_median(conn)

    #Varianza

    not_permitted_variance(conn)
    permitted_variance(conn)

    #Maximos y minimos

    permitted_max_min(conn)
    not_permitted_max_min(conn)

    print("\nCONTRASEÑAS\n")

    #add_column(conn)

    is_in_dict(conn, total)

    #Numero total observaciones

    con_debil(conn)
    not_con_debil(conn)

    #Numero missings

    con_debil_missing(conn)
    not_con_debil_missing(conn)

    #Media

    con_debil_AVG(conn)
    not_con_debil_AVG(conn)

    #Mediana

    con_debil_median(conn)
    not_con_debil_median(conn)

    #Varianza

    con_debil_variance(conn)
    not_con_debil_variance(conn)

    #Maximos y minimos

    con_debil_max_min(conn)
    not_con_debil_max_min(conn)
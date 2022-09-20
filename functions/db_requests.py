import urllib.parse

import os

urllib.parse.uses_netloc.append('mysql')

url = urllib.parse.urlparse(os.getenv('DATABASE_URL'))
  
print(url.hostname)
  
import psycopg2

host = url.hostname
dbname = url.path[1:]
user = url.username
password = url.password
sslmode = "require"

# Construct connection string
conn_string = "host={0} user={1} dbname={2} password={3} sslmode={4}".format(host, user, dbname, password, sslmode)
conn = psycopg2.connect(conn_string)
print("Connection established")

cursor = conn.cursor()

def create_user(email,assinatura_status,venda_status,forma_pagamento,data_assinatura,user_id,telefone):
  cursor.execute("INSERT INTO membros (email,assinatura_status,venda_status,forma_pagamento,data_assinatura,user_id,telefone) VALUES (%s, %s, %s, %s, %s, %s, %s);", (email,assinatura_status,venda_status,forma_pagamento,data_assinatura,user_id,telefone))
  conn.commit()

def update_user(id, email,assinatura_status,venda_status,forma_pagamento,data_assinatura,user_id,telefone):
  cursor.execute("UPDATE membros SET email=%s, assinatura_status=%s , venda_status=%s, forma_pagamento=%s, data_assinatura=%s, user_id=%s, telefone=%s WHERE id=%s;", (email,assinatura_status,venda_status,forma_pagamento,data_assinatura,user_id,telefone, id))
  conn.commit()

def find_one(id):
  cursor.execute("SELECT * FROM membros WHERE id=%s ;",(id, ))
  return cursor.fetchall()

def find_all():
  cursor.execute("SELECT*FROM membros;")
  return cursor.fetchall()


def delete_user(id):
  cursor.execute("DELETE FROM membros WHERE id=%s ;",(id,))
  conn.commit()

# cursor.close()
# conn.close()
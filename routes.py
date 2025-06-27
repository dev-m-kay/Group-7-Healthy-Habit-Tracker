import psycopg2

conn = psycopg2.connect(host="localhost", dbname="postgres", user="postgres" ,password="password", port=5432)

cur = conn.cursor()

cur.execute(open("static/db/delete.sql", "r").read())
cur.execute(open("static/db/create.sql", "r").read())
cur.execute(open("static/db/insert.sql", "r").read())

conn.commit()

cur.close()
conn.close()
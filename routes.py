import psycopg2
from flask import Flask, render_template, request, redirect

def insert():
    conn = psycopg2.connect(host="localhost", dbname="postgres", user="postgres" ,password="password", port=5432)

    cur = conn.cursor()

    cur.execute(open("static/db/delete.sql", "r").read())
    cur.execute(open("static/db/create.sql", "r").read())
    cur.execute(open("static/db/insert.sql", "r").read())

    conn.commit()

    cur.close()
    conn.close()
    pass

def delete():
    pass
def create():
    pass

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("home.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html" ), 404
@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html",),500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=11596)
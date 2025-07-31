import psycopg2
from flask import Flask, render_template, request, redirect



def delete():
    pass
def create():
    pass

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("home.html")
@app.route("/insert",methods = ["POST"])
def insert():
    if request.method == 'POST':
        #insert into Database
        pass
    return redirect("/")

@app.route("/sleep")
def sleep():
    pass

@app.route("/workout")
def workout():
    pass

@app.route("/diet")
def diet():
    pass

@app.route("/input")
def input():
    return render_template("input.html")


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html" ), 404
@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html",),500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=11596)
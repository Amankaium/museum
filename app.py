from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def homepage():
    return "<h1>Домашняя страница!</h1>"
    # return render_template("index.html")

@app.route("/contact")
def contact():
    return render_template("contact.html", name="Каюм")

@app.route("/all")
def all():
    return render_template("all.html")

@app.route("/one-image-page")
def one():
    return "Тут будет страница одной картины"
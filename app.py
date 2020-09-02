from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def homepage():
    # return "<h1>Домашняя страница!</h1>"
    return render_template("index.html")

@app.route("/contact")
def contact():
    return render_template("contact.html", name="Каюм")

@app.route("/all")
def all():
    f = open("links.txt", mode="r", encoding="utf-8")
    lst = []
    for row in f:
        splited = row.split()
        number = splited[0]
        link = splited[-1]
        txt = row[len(number)+1 : -len(link)-1]
        lst.append([number, txt, link])
    f.close()
    return render_template("all.html", lst=lst)

@app.route("/one-image-page/<id>")
def one(id):
    f = open("links.txt", mode="r", encoding="utf-8")
    lst = []
    for row in f:
        splited = row.split()
        number = splited[0]
        link = splited[-1]
        txt = row[len(number)+1 : -len(link)-1]
        lst.append([txt, link])
    f.close()
    try:
        image = lst[int(id)-1]
    except:
        return "<h1>Такой картины нет</h1>"

    return render_template("one.html", number=id, image=image)
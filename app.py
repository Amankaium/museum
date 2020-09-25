from flask import Flask, render_template, request
from openpyxl import load_workbook
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://postgres:postgres@localhost/museum_flask'
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///D:\\kaium\\projects\\python04\\projects\\museum\\museum.db'

db = SQLAlchemy(app)


class Exhibit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    url = db.Column(db.String(500), nullable=False)
    
    def __repr__(self):
        return self.name

# db.create_all()

@app.route("/all")
def all():
    lst = Exhibit.query.all()
    return render_template("exhibits.html", lst=lst)


@app.route("/")
def homepage():
    return render_template("index.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        form = request.form
        # for k in form:
        #     print(k, form[k])
        # print(form)
        user_name = form["user_name"]
    else:
        user_name = "Дорогой друг"
    return render_template("contact.html", name=user_name)

@app.route("/txt")
def txt():
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


@app.route("/excel")
def excel():
    excel_file = load_workbook("exhibits.xlsx")
    page = excel_file["Лист1"]

    lst = [[cell.value for cell in row] for row in page["A2:D11"]]

    return render_template("excel.html", lst=lst)


@app.route("/exhibit/<id>")
def one(id):
    # f = open("links.txt", mode="r", encoding="utf-8")

    # lst = []
    # for row in f:
    #     splited = row.split()
    #     number = splited[0]
    #     link = splited[-1]
    #     txt = row[len(number)+1 : -len(link)-1]
    #     lst.append([txt, link])
    # f.close()
    # try:
    #     image = lst[int(id)-1]
    # except:
    #     return "<h1>Такой картины нет</h1>"

    exhibit = Exhibit.query.filter_by(id=id).first()

    return render_template("one.html", exhibit=exhibit)


@app.route("/create")
def create_form():
    return render_template("create_form.html")


@app.route("/add", methods=["POST"])
def add():
    # f = open("links.txt", mode="r+", encoding="utf-8")

    # rows = f.read().split("\n")
    # last_eksponat = rows[-2]
    # last_eksponat_list = last_eksponat.split()
    # last_num = int(last_eksponat_list[0])

    # # f.write("7 " + form["name"] + " " + form["url"] + "\n")
    # f.write(f"{last_num + 1} {form['name']} {form['url']}\n") # 7 Кисточки http:////art2bid.com/assets/images/slid..
    # f.close()
    form = request.form
    name = form["name"]
    url = form["url"]
    e = Exhibit(name=name, url=url)
    db.session.add(e)
    db.session.commit()
    return "<h2>Ваша форма обработана</h2>"


@app.route("/exhibit/<id>/delete")
def delete(id):
    exhibit = Exhibit.query.filter_by(id=id).first()
    db.session.delete(exhibit)
    db.session.commit()
    return "<h1>Экспонат удалён!</h1>"


@app.route("/exhibit/<id>/update_form")
def update_form(id):
    exhibit = Exhibit.query.filter_by(id=id).first()
    return render_template("update_form.html", exhibit=exhibit)

@app.route("/exhibit/<id>/update", methods=["POST"])
def update(id):
    name = request.form["name"]
    url = request.form["url"]
    exhibit = Exhibit.query.filter_by(id=id).first()
    exhibit.name = name
    exhibit.url = url
    db.session.commit()
    return "<h1>Изменения сохранены!</h1>"
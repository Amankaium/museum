from flask import Flask, render_template, request
from openpyxl import load_workbook

app = Flask(__name__)

@app.route("/")
def homepage():
    # return "<h1>Домашняя страница!</h1>"
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


@app.route("/excel")
def excel():
    excel_file = load_workbook("exhibits.xlsx")
    page = excel_file["Лист1"]

    lst = [[cell.value for cell in row] for row in page["A2:D11"]]

    return render_template("excel.html", lst=lst)


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


@app.route("/create")
def create_form():
    return render_template("create_form.html")


@app.route("/add", methods=["POST"])
def add():
    form = request.form
    f = open("links.txt", mode="r+", encoding="utf-8")

    rows = f.read().split("\n")
    last_eksponat = rows[-2]
    last_eksponat_list = last_eksponat.split()
    last_num = int(last_eksponat_list[0])

    # f.write("7 " + form["name"] + " " + form["url"] + "\n")
    f.write(f"{last_num + 1} {form['name']} {form['url']}\n") # 7 Кисточки http:////art2bid.com/assets/images/slid..
    f.close()
    return "<h2>Ваша форма обработана</h2>"


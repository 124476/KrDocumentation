import sqlite3

from flask import Flask, render_template, redirect, make_response, request, send_file
from flask_restful import abort, Api

app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

a = {"1235": ["Best Diary", 5000, 3],
     "1243": ["Entangled Tale", 3000, 1],
     "1254": ["Редактор текста", 300, 1],
     "1345": ["Помощник в учебе 2", 1500, 1],
     "1351": ["Помощник учителя", 1000, 1],
     "1367": ["Secret chat", 0, 2],
     "1435": ["Тг бот \"Столовая\"", 1500, 3],
     "1513": ["Шпион бот", 1500, 3],
     "5234": ["Троль программа", 2000, 3],
     "6513": ["Документация", 1500, 2]}


def main():
    app.run()


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template("index.html")
    project = request.form.get('project')
    if project in a:
        return redirect("/project/" + project)
    return render_template("index.html", errorText="Такой проект не найден")


@app.route("/project/<string:idProject>")
def info_project(idProject):
    if idProject in a:
        return render_template(idProject + ".html", title=idProject)
    return redirect("/")


@app.route("/shop", methods=['GET', 'POST'])
def shop():
    return render_template("shop.html", towars=a)


@app.route("/school", methods=['GET', 'POST'])
def school():
    if request.method == 'GET':
        user = ""
    else:
        user = request.form.get('userName')

    con = sqlite3.connect("db/Dbase.db")
    cur = con.cursor()
    res = cur.execute("SELECT name, description FROM user").fetchall()
    con.close()

    userNames = [i[0] for i in res]

    users = [i for i in userNames if user.lower() in i.lower()]
    if len(users) != 0:
        return render_template("school.html", res=users)

    return render_template("school.html", errorText="Никто не найден")


@app.route("/users/<string:userName>", methods=['GET', 'POST'])
def get_user(userName):
    userName = userName.strip()
    con = sqlite3.connect("db/Dbase.db")
    cur = con.cursor()
    res = cur.execute(f"SELECT name, description FROM user WHERE name = '{userName}'").fetchall()
    con.close()
    return render_template("info_user.html", res=res[0])


if __name__ == '__main__':
    app.run()

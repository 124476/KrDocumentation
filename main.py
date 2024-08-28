import os
import sqlite3

from flask import Flask, render_template, redirect, make_response, request, send_file, url_for
from flask_restful import abort, Api
from werkzeug.utils import secure_filename

app = Flask(__name__)
api = Api(app)

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


UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
can_uplode = True


def allowed_file(filename):
    """ Функция проверки расширения файла """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/materials", methods=['GET', 'POST'])
def materials():
    error_text = ""
    files = [name for name in os.listdir("static/files") if os.path.isfile(os.path.join("static/files", name))]

    if request.method == 'POST':
        if 'file' in request.files:
            file = request.files['file']
            name = request.form['name']
            if file.filename != '':
                if file:
                    filename = secure_filename(file.filename)
                    filename = filename.split('.')[-1]
                    file.save(os.path.join("static/files", name + "." + filename))
                    return redirect("/materials")
        error_text = "Ошибка загрузки"

    count = len([name for name in os.listdir("static/files") if os.path.isfile(os.path.join("static/files", name))])
    return render_template("materials.html", files=files, count=count, errorText=error_text, canUplode=can_uplode)


@app.route("/materials/<string:tip>", methods=['GET', 'POST'])
def materials_get(tip):
    global can_uplode
    if tip == "yes":
        can_uplode = True
    elif tip == "no":
        can_uplode = False

    return redirect("/materials")


@app.route("/materials/del/<string:material>", methods=['GET', 'POST'])
def materials_del(material):
    files = [name for name in os.listdir("static/files") if os.path.isfile(os.path.join("static/files", name))]
    if material in files:
        os.remove("static/files/" + material)

    return redirect("/materials")


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

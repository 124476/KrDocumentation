from flask import Flask, render_template, redirect, make_response, request, send_file
from flask_restful import abort, Api

app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

a = ["1235", "1243", "1345", "1351", "1367", "1435", "1513", "5234", "6513"]


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


if __name__ == '__main__':
    app.run()

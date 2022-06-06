from datetime import datetime
from types import SimpleNamespace
from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def main():
    demandas = [
        SimpleNamespace(
            titulo="Alterar tabela",
            tipo="Alteração De Operação da Empresa",
            responsavel="Leonardo",
            data=datetime(2022, 5, 12, 15, 0),
        ),
        SimpleNamespace(
            titulo="Responder MP",
            tipo=None,
            responsavel="Jayme",
            data=datetime(2022, 5, 13, 11, 9),
        ),
    ]
    return render_template("home.html", demandas=demandas)


@app.route("/demanda")
def demanda():
    return render_template("demanda_view.html")

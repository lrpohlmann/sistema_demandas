from datetime import datetime
from types import SimpleNamespace
from flask import Flask, render_template
from sqlalchemy.orm import scoped_session

from sistema.persistencia import setup_persistencia


def criar_web_app(test_config=None) -> Flask:
    app = _setup_web_app(test_config)
    db = _setup_app_db(app)
    _setup_app_views(app, db)
    return app


def _setup_web_app(test_config=None):
    app = Flask(__name__)
    if test_config:
        app.config.from_mapping(test_config)
    else:
        pass

    return app


def _setup_app_db(app: Flask):
    db = setup_persistencia(app.config["DB"])

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db.remove()

    return db


def _setup_app_views(app: Flask, db: scoped_session):
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

    @app.route("/demanda/<int:demanda>", methods=["GET", "PUT", "DELETE"])
    def demanda_view():
        return render_template("demanda_view.html")

    @app.route(
        "/demanda",
        methods=[
            "POST",
        ],
    )
    def demanda():
        ...

    @app.route("/tarefa", methods=["POST"])
    def tarefa():
        ...

    @app.route("/tarefa/<int:id_tarefa>", methods=["GET", "PUT", "DELETE"])
    def tarefa_view():
        ...

    return app

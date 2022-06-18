from datetime import datetime
from types import SimpleNamespace
from flask import Flask, render_template, request
from sqlalchemy.orm import scoped_session
from sistema.model.entidades.demanda import Demanda

from sistema.persistencia import setup_persistencia


def criar_web_app(test_config=None) -> Flask:
    app = _setup_web_app(test_config)
    db, mapper, metadata = _setup_app_db(app)
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
    db, mapper, metadata = setup_persistencia(app.config["DB"])

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db.remove()

    return db, mapper, metadata


def _setup_app_views(app: Flask, db: scoped_session):
    @app.route("/")
    def main():
        demandas = db.query(Demanda).all()
        return render_template("home.html", demandas=demandas)

    @app.route("/demanda/<int:demanda>", methods=["GET", "PUT", "DELETE"])
    def demanda_view():
        return render_template("demanda_view.html")

    @app.route(
        "/demanda",
        methods=["POST", "GET"],
    )
    def demanda():
        if request.method == "GET":
            demandas = db.query(Demanda).all()
            return render_template("componentes/demandas.html", demandas=demandas)

    @app.route("/tarefa", methods=["POST"])
    def tarefa():
        ...

    @app.route("/tarefa/<int:id_tarefa>", methods=["GET", "PUT", "DELETE"])
    def tarefa_view():
        ...

    return app

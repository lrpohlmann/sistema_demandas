from datetime import datetime
from flask import Flask, render_template, request
from sqlalchemy.orm import scoped_session

from sistema.model.entidades.demanda import Demanda, TipoDemanda
from sistema.model.entidades.usuario import Usuario
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
            dados_consulta = dict(**request.args)

            consulta = db.query(Demanda)
            if dados_consulta.get("titulo"):
                consulta = consulta.filter(
                    Demanda.titulo.like("%{}%".format(dados_consulta.get("titulo")))
                )
            elif dados_consulta.get("tipo_id"):
                consulta = consulta.filter(
                    Demanda.tipo_id == int(dados_consulta.get("tipo_id"))
                )
            elif dados_consulta.get("responsavel_id"):
                consulta = consulta.filter(
                    Demanda.responsavel_id == int(dados_consulta.get("responsavel_id"))
                )
            elif dados_consulta.get("data_criacao"):
                consulta.filter(
                    Demanda.data_criacao
                    == datetime.strptime(
                        dados_consulta["data_entrega"], "%Y-%m-%d %H:%M:%S"
                    )
                )
            demandas = consulta.all()
            return render_template("componentes/demandas.html", demandas=demandas)
        elif request.method == "POST":
            dados_form = dict(**request.form)
            if dados_form.get("dia_entrega") and dados_form.get("horario_entrega"):
                dados_form["data_entrega"] = datetime.strptime(
                    dados_form["dia_entrega"] + " " + dados_form["horario_entrega"],
                    "%Y-%m-%d %H:%M",
                )
            elif dados_form.get("dia_entrega"):
                dados_form["data_entrega"] = datetime.strptime(
                    dados_form["dia_entrega"],
                    "%Y-%m-%d",
                )

            nova_demanda = Demanda(
                titulo=dados_form["titulo"],
                tipo=db.query(TipoDemanda).get(int(dados_form["tipo_id"])),
                responsavel=db.query(Usuario).get(int(dados_form["responsavel_id"])),
                data_entrega=dados_form["data_entrega"],
            )
            db.add(nova_demanda)
            db.commit()
            return "", 201

    @app.route("/tarefa", methods=["POST"])
    def tarefa():
        ...

    @app.route("/tarefa/<int:id_tarefa>", methods=["GET", "PUT", "DELETE"])
    def tarefa_view():
        ...

    return app

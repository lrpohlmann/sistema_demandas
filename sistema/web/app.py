from datetime import datetime
from typing import Sequence
from flask import Flask, render_template, request
from sqlalchemy import select
from sqlalchemy.orm import scoped_session

from sistema.model.entidades.demanda import Demanda, TipoDemanda
from sistema.model.entidades.usuario import Usuario
from sistema.persistencia import setup_persistencia
from sistema.web.forms.consulta_demanda import ConsultaDemandaForm


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
            consulta = db.query(Demanda)

            if request.args:
                tp_demanda: Sequence[TipoDemanda] = db.query(TipoDemanda).all()
                responsaveis: Sequence[Usuario] = db.query(Usuario).all()

                form = ConsultaDemandaForm(**request.args)

                form.responsavel_id.choices = [
                    (r.id_usuario, r.nome) for r in responsaveis
                ] + [
                    ("", "-"),
                ]
                form.tipo_id.choices = [
                    (t.id_tipo_demanda, t.nome) for t in tp_demanda
                ] + [
                    ("", "-"),
                ]

                form.validate()
                if form.titulo.data:
                    consulta = consulta.filter(Demanda.titulo.like(form.titulo.data))
                elif form.tipo_id.data:
                    consulta = consulta.filter(Demanda.tipo_id == form.tipo_id.data)
                elif form.responsavel_id.data:
                    consulta = consulta.filter(
                        Demanda.responsavel_id == form.responsavel_id.data
                    )
                elif form.data_criacao.data:
                    consulta.filter(Demanda.data_criacao == form.data_criacao.data)
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

    @app.route("/tipo_demanda", methods=["GET"])
    def tipo_demanda():
        tp_demanda = db.query(TipoDemanda).all()

        formato = request.args.get("formato")
        if request.method == "GET":
            if formato == "select":
                return render_template(
                    "componentes/option_tipo_demanda.html", tipo_demanda=tp_demanda
                )

    @app.route("/usuario/formato/<tipo_formato>")
    def usuario(tipo_formato: str):
        if tipo_formato == "option":
            usuarios = db.execute(
                select(Usuario.id_usuario, Usuario.nome).order_by(Usuario.id_usuario)
            ).fetchall()
            return render_template("componentes/option_usuario.html", usuario=usuarios)

    @app.route(
        "/form/<nome>",
        methods=[
            "GET",
        ],
    )
    def forms(nome: str):
        if nome == "consulta_demanda":
            tp_demanda: Sequence[TipoDemanda] = db.query(TipoDemanda).all()
            responsaveis: Sequence[Usuario] = db.query(Usuario).all()

            form_consulta_demanda = ConsultaDemandaForm()
            form_consulta_demanda.responsavel_id.choices = [
                (r.id_usuario, r.nome) for r in responsaveis
            ] + [
                ("", "-"),
            ]
            form_consulta_demanda.tipo_id.choices = [
                (t.id_tipo_demanda, t.nome) for t in tp_demanda
            ] + [
                ("", "-"),
            ]
            return render_template(
                "componentes/forms/form_consulta_demandas.html",
                form_consulta_demanda=form_consulta_demanda,
            )

    @app.route("/tarefa", methods=["POST"])
    def tarefa():
        ...

    @app.route("/tarefa/<int:id_tarefa>", methods=["GET", "PUT", "DELETE"])
    def tarefa_view():
        ...

    return app

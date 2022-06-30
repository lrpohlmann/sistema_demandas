from typing import Sequence
from flask import render_template, request, redirect, url_for

from sistema.model.entidades.demanda import Demanda, TipoDemanda
from sistema.model.entidades.usuario import Usuario
from sistema.web.forms.consulta_demanda import ConsultaDemandaForm
from sistema.web.forms.criar_demanda import CriarDemandaForm


def setup_views(app, db):
    @app.route("/demanda/<int:demanda_id>", methods=["GET", "PUT", "DELETE"])
    def demanda_view(demanda_id: int):
        demanda = db.get(Demanda, demanda_id)
        if demanda:
            return render_template("demanda_view.html", demanda=demanda)
        else:
            return "", 404

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
            tp_demanda: Sequence[TipoDemanda] = db.query(TipoDemanda).all()
            responsaveis: Sequence[Usuario] = db.query(Usuario).all()

            form_criar_demanda = CriarDemandaForm(**request.form)
            form_criar_demanda.responsavel_id.choices = [
                (r.id_usuario, r.nome) for r in responsaveis
            ] + [
                ("", "-"),
            ]
            form_criar_demanda.tipo_id.choices = [
                (t.id_tipo_demanda, t.nome) for t in tp_demanda
            ] + [
                ("", "-"),
            ]
            if form_criar_demanda.validate():
                nova_demanda = Demanda(
                    titulo=form_criar_demanda.titulo.data,
                    tipo=db.query(TipoDemanda).get(form_criar_demanda.tipo_id.data),
                    responsavel=db.query(Usuario).get(
                        form_criar_demanda.responsavel_id.data
                    ),
                    data_entrega=form_criar_demanda.data_entrega.data,
                )

                db.add(nova_demanda)
                db.commit()
                return redirect(
                    url_for("demanda_view", demanda_id=nova_demanda.id_demanda)
                )

            else:
                return render_template(
                    "componentes/forms/form_criar_demandas.html",
                    form_criar_demanda=form_criar_demanda,
                )

    @app.route("/tipo_demanda", methods=["GET"])
    def tipo_demanda():
        tp_demanda = db.query(TipoDemanda).all()

        formato = request.args.get("formato")
        if request.method == "GET":
            if formato == "select":
                return render_template(
                    "componentes/option_tipo_demanda.html", tipo_demanda=tp_demanda
                )

    return app, db

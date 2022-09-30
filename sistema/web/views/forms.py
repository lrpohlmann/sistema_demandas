from typing import Sequence

from flask import render_template
from flask_login import login_required

from sistema.model.entidades.demanda import TipoDemanda
from sistema.model.entidades.usuario import Usuario
from sistema.web.forms.consulta_demanda import ConsultaDemandaForm
from sistema.web.forms.criar_demanda import CriarDemandaForm


def setup_views(app, db):
    @app.route(
        "/form/<nome>",
        methods=[
            "GET",
        ],
    )
    @login_required
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
        elif nome == "criar_demanda":
            tp_demanda: Sequence[TipoDemanda] = db.query(TipoDemanda).all()
            responsaveis: Sequence[Usuario] = db.query(Usuario).all()

            form_criar_demanda = CriarDemandaForm()

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

            return render_template(
                "componentes/forms/form_criar_demandas.html",
                form_criar_demanda=form_criar_demanda,
            )

    return app, db

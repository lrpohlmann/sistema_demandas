from typing import Sequence
from flask import render_template_string, abort
from flask_login import login_required

from sistema.model.entidades import TipoDemanda, Demanda, Usuario
from sistema.web import renderizacao
from sistema.web.forms import editar_dados_demanda


def setup_views(app, db):
    @app.route(
        "/demanda/editar/form/<int:demanda_id>",
        methods=[
            "GET",
        ],
    )
    @login_required
    def editar_demanda_form(demanda_id: int):
        demanda: Demanda = db.get(Demanda, demanda_id)
        if not demanda:
            return abort(404)

        tp_demanda: Sequence[TipoDemanda] = db.query(TipoDemanda).all()
        responsaveis: Sequence[Usuario] = db.query(Usuario).all()
        form = editar_dados_demanda.criar_form(
            escolhas_responsavel=[(r.id_usuario, r.nome) for r in responsaveis]
            + [
                ("", "-"),
            ],
            escolhas_tipo=[(t.id_tipo_demanda, t.nome) for t in tp_demanda],
            escolhas_status=[("PENDENTE", "Pendente"), ("REALIZADA", "realizada")],
            responsavel_id=demanda.responsavel_id if demanda.responsavel_id else "",
            tipo_id=demanda.tipo_id,
            status=demanda.status,
        )
        return renderizacao.renderizar_editar_demanda_form(form, demanda_id)

    return app, db

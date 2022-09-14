from typing import Sequence

from flask import render_template_string

from sistema.model.entidades.demanda import TipoDemanda
from sistema.model.entidades.usuario import Usuario
from sistema.web import renderizacao
from sistema.web.forms import editar_dados_demanda


def setup_views(app, db):
    @app.route(
        "/demanda/editar/form/<int:demanda_id>",
        methods=[
            "GET",
        ],
    )
    def editar_demanda_form(demanda_id: int):
        tp_demanda: Sequence[TipoDemanda] = db.query(TipoDemanda).all()
        responsaveis: Sequence[Usuario] = db.query(Usuario).all()
        form = editar_dados_demanda.criar_form(
            escolhas_responsavel=[(r.id_usuario, r.nome) for r in responsaveis]
            + [
                ("", "-"),
            ],
            escolhas_tipo=[(t.id_tipo_demanda, t.nome) for t in tp_demanda],
        )
        return renderizacao.renderizar_editar_demanda_form(form, demanda_id)

    return app, db

from flask import render_template_string, request

from sistema.model.operacoes.demanda import (
    tornar_demanda_pendente,
    tornar_demanda_realizada,
)
from sistema.model.entidades.demanda import Demanda, TipoDemanda
from sistema.model.entidades.usuario import Usuario
from sistema.web import renderizacao
from sistema.web.forms import editar_dados_demanda


def setup_views(app, db):
    @app.route("/demanda/editar/salvar/<int:demanda_id>", methods=["PUT"])
    def salvar_edicao_demanda(demanda_id: int):
        form = editar_dados_demanda.criar_form(
            escolhas_responsavel=[
                (r.id_usuario, r.nome) for r in db.query(Usuario).all()
            ]
            + [("", "-")],
            escolhas_tipo=[
                (t.id_tipo_demanda, t.nome) for t in db.query(TipoDemanda).all()
            ],
            escolhas_status=[("PENDENTE", "Pendente"), ("REALIZADA", "realizada")],
            **request.form,
        )
        if form.validate():
            demanda: Demanda = db.get(Demanda, demanda_id)
            demanda.tipo = db.get(TipoDemanda, form.tipo_id.data)
            demanda.responsavel = (
                db.get(Usuario, form.responsavel_id.data)
                if form.responsavel_id.data
                else None
            )
            if form.status.data == "PENDENTE":
                tornar_demanda_pendente(demanda)
            else:
                tornar_demanda_realizada(demanda)
            db.commit()

            return renderizacao.rendereizar_lista_dados_demanda(demanda, demanda_id)
        else:
            return renderizacao.renderizar_editar_demanda_form(form, demanda_id)

    return app, db

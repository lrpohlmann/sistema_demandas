from flask import request
from flask_login import login_required

from sistema.model.entidades.demanda import Demanda
from sistema.model.entidades.tarefa import Tarefa
from sistema.model.entidades.usuario import Usuario
from sistema.web import renderizacao
from sistema.web.forms import criar_tarefa


def setup_views(app, db):
    @app.route("/demanda/<int:demanda_id>/tarefas/criar", methods=["POST"])
    @login_required
    def criar_tarefa_view(demanda_id: int):
        demanda: Demanda = db.get(Demanda, demanda_id)
        if not demanda:
            return "", 404

        form = criar_tarefa.criar_form(
            escolhas_responsavel=[
                (u.id_usuario, u.nome) for u in db.query(Usuario).all()
            ]
            + [("", "-")],
            **request.form
        )
        if criar_tarefa.e_valido(form):
            dados = criar_tarefa.obter_dados(form)
            tarefa_criada = Tarefa(
                responsavel=db.get(Usuario, dados.get("responsavel_id"))
                if dados.get("responsavel_id")
                else None,
                titulo=dados.get("titulo"),
                data_entrega=dados.get("data_entrega"),
                descricao=dados.get("descricao"),
            )
            demanda.tarefas.append(
                tarefa_criada,
            )
            db.add(tarefa_criada)
            db.commit()

            return (
                renderizacao.renderizar_criar_tarefa_form(form, demanda_id),
                202,
                {"HX-Trigger": "tarefaCriada"},
            )

        return renderizacao.renderizar_criar_tarefa_form(form, demanda_id)

    return app, db

from flask import render_template_string, request
from flask_login import login_required
import sqlalchemy

from sistema.model.entidades.tarefa import StatusTarefa, Tarefa
from sistema.web import renderizacao
from sistema.servicos import paginacao


def setup_views(app, db):
    @app.route("/demanda/<int:demanda_id>/tarefas/cards", methods=["GET"])
    @login_required
    def tarefa_card_view(demanda_id: int):
        tarefas = (
            db.execute(
                sqlalchemy.select(Tarefa)
                .where(
                    Tarefa.demanda_id == demanda_id,
                    Tarefa.status == StatusTarefa.EM_ABERTO,
                )
                .order_by(Tarefa.data_hora)
            )
            .scalars()
            .all()
        )

        tarefas_paginadas = paginacao.paginar(tarefas, 5)

        pagina_selecionada = request.args.get("pagina")
        if pagina_selecionada is not None:
            pagina_selecionada = int(pagina_selecionada)
            if pagina_selecionada > tarefas_paginadas["numero_paginas"]:
                pagina_selecionada = 1
        else:
            pagina_selecionada = 1

        return renderizacao.sequencia_tarefa_card_com_paginacao(
            tarefas_paginadas["paginador"](pagina_selecionada),
            pagina_selecionada,
            tarefas_paginadas["numero_paginas"],
            "tarefa_card_view",
            {"demanda_id": demanda_id},
            "tarefaCriada from:body, TarefaFinalizada from:body, TarefaDeletada from:body",
        )

    return app, db

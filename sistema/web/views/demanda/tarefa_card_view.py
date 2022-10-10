from flask import render_template_string
from flask_login import login_required
import sqlalchemy

from sistema.model.entidades.tarefa import StatusTarefa, Tarefa
from sistema.web import renderizacao


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
        return renderizacao.renderizar_sequencia_tarefas_card(tarefas)

    return app, db

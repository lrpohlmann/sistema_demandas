from flask import Flask, render_template_string, abort, request
from sqlalchemy.orm import scoped_session
import sqlalchemy
from flask_login import login_required

from sistema.model.entidades import Tarefa, StatusTarefa, Demanda
from sistema.model.operacoes.tarefa import set_status, finalizar_tarefa
from .. import renderizacao
from sistema.servicos import pagincao


def setup_views(app: Flask, db: scoped_session):
    @app.route("/tarefa/deletar/<int:tarefa_id>", methods=["DELETE"])
    @login_required
    def deletar_tarefa_view(tarefa_id: int):
        tarefa = db.get(Tarefa, tarefa_id)
        if tarefa:
            db.delete(tarefa)
            db.commit()
            return "", 200, {"HX-Trigger": "TarefaDeletada"}
        else:
            return "", 404

    @app.route("/tarefa/status/finalizar/<int:tarefa_id>", methods=["PUT"])
    @login_required
    def finalizar_tarefa_view(tarefa_id: int):
        tarefa = db.get(Tarefa, tarefa_id)
        if tarefa:
            finalizar_tarefa(tarefa)
            db.commit()
            return (
                "",
                200,
                {"HX-Trigger": "TarefaFinalizada"},
            )
        else:
            return "", 404

    @app.route("/tarefa/cards/finalizadas/por-demanda/<int:demanda_id>")
    @login_required
    def obter_tarefas_finalizadas_por_demanda_view(demanda_id: int):
        demanda = db.get(Demanda, demanda_id)
        if not demanda:
            return abort(404)

        tarefas_finalizadas = (
            db.execute(
                sqlalchemy.select(Tarefa).where(
                    Tarefa.demanda_id == demanda_id,
                    Tarefa.status == StatusTarefa.FINALIZADA,
                )
            )
            .scalars()
            .all()
        )

        tarefas_finalizadas_paginadas = pagincao.paginar(tarefas_finalizadas, 5)
        numero_de_paginas = tarefas_finalizadas_paginadas["numero_paginas"]
        pagina_pedida = pagincao.validar_pagina_pedida(
            request.args.get("pagina"), numero_de_paginas
        )
        pagina_com_tarefas = tarefas_finalizadas_paginadas["paginador"](pagina_pedida)

        return renderizacao.sequencia_tarefa_card_com_paginacao(
            pagina_com_tarefas,
            pagina_pedida,
            numero_de_paginas,
            "obter_tarefas_finalizadas_por_demanda_view",
            {"demanda_id": demanda_id},
            "TarefaFinalizada from:body, TarefaDeletada from:body",
        )

    return app, db

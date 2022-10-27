from flask import Flask, render_template_string, abort, request
from sqlalchemy.orm import scoped_session
import sqlalchemy
from flask_login import login_required, current_user

from sistema.model.entidades import Tarefa, StatusTarefa, Demanda, Usuario
from sistema.model.operacoes.tarefa import set_status, finalizar_tarefa
from sistema.web.forms import criar_tarefa
from .. import renderizacao
from sistema.servicos import paginacao
from sistema.web import eventos_cliente


def setup_views(app: Flask, db: scoped_session):
    @app.route("/tarefas/criar/<int:demanda_id>", methods=["POST"])
    @login_required
    def criar_tarefa_view(demanda_id: int):
        demanda: Demanda = db.get(Demanda, demanda_id)
        if not demanda:
            return abort(404)

        form = criar_tarefa.criar_form(
            escolhas_responsavel=[
                (u.id_usuario, u.nome) for u in db.query(Usuario).all()
            ]
            + [("", "-")],
            dados_input_usuario=request.form,
        )
        if criar_tarefa.e_valido(form):
            dados = criar_tarefa.obter_dados(form)
            tarefa_criada = Tarefa(
                responsavel=db.get(Usuario, dados.get("responsavel_id"))
                if dados.get("responsavel_id")
                else None,
                titulo=dados["titulo"],
                data_entrega=dados["data_entrega"],
                descricao=dados["descricao"],
                demanda=demanda,
            )
            db.add(tarefa_criada)
            db.commit()

            return (
                renderizacao.renderizar_criar_tarefa_form(form, demanda_id),
                201,
                {"HX-Trigger": eventos_cliente.TAREFA_CRIADA},
            )

        return renderizacao.renderizar_criar_tarefa_form(form, demanda_id)

    @app.route("/tarefa/deletar/<int:tarefa_id>", methods=["DELETE"])
    @login_required
    def deletar_tarefa_view(tarefa_id: int):
        tarefa = db.get(Tarefa, tarefa_id)
        if tarefa:
            db.delete(tarefa)
            db.commit()
            return "", 200, {"HX-Trigger": eventos_cliente.TAREFA_DELETADA}
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
                {"HX-Trigger": eventos_cliente.TAREFA_FINALIZADA},
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

        tarefas_finalizadas_paginadas = paginacao.paginar(tarefas_finalizadas, 5)
        numero_de_paginas = tarefas_finalizadas_paginadas["numero_paginas"]
        pagina_pedida = paginacao.validar_pagina_pedida(
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

    @app.route("/tarefa/minhas-tarefas/tabela", methods=["GET"])
    @login_required
    def obter_minhas_tarefas_em_aberto_view():
        minhas_tarefas_em_aberto = (
            db.execute(
                sqlalchemy.select(Tarefa).where(
                    Tarefa.responsavel == current_user,
                    Tarefa.status == StatusTarefa.EM_ABERTO,
                )
            )
            .scalars()
            .all()
        )

        tarefas_paginadas = paginacao.paginar(minhas_tarefas_em_aberto, 10)
        numero_de_paginas = tarefas_paginadas["numero_paginas"]
        pagina_requerida = paginacao.validar_pagina_pedida(
            request.args.get("pagina"), numero_de_paginas
        )
        tarefas_pagina_requerida = tarefas_paginadas["paginador"](pagina_requerida)

        return renderizacao.renderizar_tabela_de_tarefas(
            tarefas_pagina_requerida,
            pagina_requerida,
            numero_de_paginas,
            "obter_minhas_tarefas_em_aberto_view",
            {},
            "closest div[data-hx-elemento-alvo]",
        )

    return app, db

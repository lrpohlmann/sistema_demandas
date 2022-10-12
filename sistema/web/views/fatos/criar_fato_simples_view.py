from flask import request
from flask_login import login_required

from sistema.model.entidades.demanda import Demanda, TipoDemanda
from sistema.web import renderizacao
from sistema.web.forms import criar_fato_simples_form
from sistema.model.entidades.fato import Fato, TipoFatos
from sistema.model.operacoes.tarefa import inserir_fatos
from sistema.web import eventos_cliente


def setup_views(app, db):
    @app.route("/fato/criar/simples", methods=["POST"])
    @login_required
    def criar_fato_simples_view():
        form = criar_fato_simples_form.criar_form(**request.form)
        if criar_fato_simples_form.e_valido(form):
            dados = criar_fato_simples_form.obter_dados(form)
            demanda: Demanda = db.get(Demanda, dados["demanda_id"])
            if not demanda:
                return (
                    renderizacao.renderizar_criar_fato_simples_form(form),
                    404,
                )
            demanda_com_fato_novo = inserir_fatos(
                demanda,
                Fato(
                    titulo=dados["titulo"],
                    tipo=TipoFatos.SIMPLES,
                    descricao=dados["descricao"],
                ),
            )
            db.commit()
            return (
                renderizacao.renderizar_criar_fato_simples_form(form),
                202,
                {"HX-Trigger": eventos_cliente.FATO_CRIADO},
            )
        return (
            renderizacao.renderizar_criar_fato_simples_form(form),
            404,
        )

    return app, db

from flask_login import login_required
import flask

from sistema.web.forms import criar_tipo_demanda
from sistema.model.entidades import TipoDemanda
from sistema.web import renderizacao, eventos_cliente


def setup_views(app, db):
    @app.route("/tipo-demanda/criar", methods=["GET", "POST"])
    @login_required
    def criar_tipo_demanda_view():
        form = criar_tipo_demanda.criar_form(flask.request.form)
        if flask.request.method == "POST" and criar_tipo_demanda.e_valido(form):
            dados = criar_tipo_demanda.obter_dados(form)
            db.add(TipoDemanda(dados["nome"]))
            db.commit()

            return (
                renderizacao.renderizar_criar_tipo_demanda_form(form),
                201,
                {"HX-Trigger": eventos_cliente.TIPO_DEMANDA_CRIADO},
            )

        return renderizacao.renderizar_criar_tipo_demanda_form(form)

    return app, db

from flask_login import login_required
import flask
import sqlalchemy
from sistema.model.entidades.demanda import Demanda

from sistema.web.forms import criar_demanda
from sistema.model.entidades import Usuario, TipoDemanda
from sistema.web import renderizacao


def setup_views(app, db):
    @app.route("/demanda/criar", methods=["POST"])
    @login_required
    def criar_demanda_view():
        form = criar_demanda.criar_form(
            responsavel_id_escolhas=[
                (consulta[0], consulta[1])
                for consulta in db.execute(
                    sqlalchemy.select(Usuario.id_usuario, Usuario.nome)
                )
            ]
            + [("", "-")],
            tipo_id_escolhas=[
                (consulta[0], consulta[1])
                for consulta in db.execute(
                    sqlalchemy.select(TipoDemanda.id_tipo_demanda, TipoDemanda.nome)
                )
            ],
            dados_input_usuario=flask.request.form,
        )
        if criar_demanda.e_valido(form):
            dados = criar_demanda.obter_dados(form)
            db.add(
                nova_demanda := Demanda(
                    titulo=dados["titulo"],
                    tipo=db.get(TipoDemanda, dados["tipo_id"]),
                    responsavel=db.get(Usuario, dados["responsavel_id"])
                    if dados["responsavel_id"]
                    else None,
                    data_entrega=dados["data_entrega"],
                )
            )
            db.commit()

            return (
                "",
                201,
                {
                    "HX-Redirect": app.url_for(
                        "demanda_view", demanda_id=nova_demanda.id_demanda
                    )
                },
            )
        else:
            return renderizacao.renderizar_form_criar_demanda(form)

    return app, db

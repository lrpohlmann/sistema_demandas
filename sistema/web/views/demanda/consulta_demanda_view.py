import flask
import sqlalchemy
from flask_login import login_required

from sistema.model.entidades import demanda, usuario
from sistema.web import renderizacao
from sistema.web.forms.consulta_demanda_form import criar_form, e_valido, obter_dados
from sistema.persistencia import operacoes


def setup_views(app, db):
    @app.route("/demanda/form/consulta-demanda", methods=["GET"])
    @login_required
    def obter_form_consulta_demanda():
        form_consulta_demanda = criar_form(
            [
                ("", "-"),
            ]
            + [
                (r[0], r[1])
                for r in db.execute(
                    sqlalchemy.select(usuario.Usuario.id_usuario, usuario.Usuario.nome)
                ).fetchall()
            ],
            [
                ("", "-"),
            ]
            + [
                (r[0], r[1])
                for r in db.execute(
                    sqlalchemy.select(
                        demanda.TipoDemanda.id_tipo_demanda, demanda.TipoDemanda.nome
                    )
                ).fetchall()
            ],
        )

        return renderizacao.renderizar_form_consulta_demanda(form_consulta_demanda)

    @app.route("/demanda/consulta", methods=["GET"])
    @login_required
    def consulta_demanda():
        consulta = sqlalchemy.select(demanda.Demanda).order_by(
            demanda.Demanda.data_criacao
        )

        form_consulta_demanda = criar_form(
            [
                ("", "-"),
            ]
            + [
                (r[0], r[1])
                for r in db.execute(
                    sqlalchemy.select(usuario.Usuario.id_usuario, usuario.Usuario.nome)
                ).fetchall()
            ],
            [
                ("", "-"),
            ]
            + [
                (r[0], r[1])
                for r in db.execute(
                    sqlalchemy.select(
                        demanda.TipoDemanda.id_tipo_demanda, demanda.TipoDemanda.nome
                    )
                ).fetchall()
            ],
            **flask.request.args,
        )
        if e_valido(form_consulta_demanda):
            dados = obter_dados(form_consulta_demanda)
            demandas = operacoes.consultar_demandas(db, dados)

            return renderizacao.renderizar_tabela_de_demandas(
                demandas=demandas,
                numero_paginas=1,
                pagina_atual=1,
                nome_da_view="consulta_demanda",
                kwargs_url={},
            )
        else:
            return "", 400

    return app, db

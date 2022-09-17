import flask
import sqlalchemy

from sistema.model.entidades import demanda, documento, fato, tarefa, usuario
from sistema import servicos
from sistema.web import renderizacao


def setup_views(app, db):
    @app.route("/demanda/consulta", methods=["GET"])
    def consulta_demanda():
        consulta = sqlalchemy.select(demanda.Demanda).order_by(
            demanda.Demanda.data_criacao
        )
        if flask.request.args:
            dados = flask.request.args
            if dados.get("titulo"):
                consulta = consulta.where(demanda.Demanda.titulo == dados.get("titulo"))

            if dados.get("responsavel_id"):
                consulta = consulta.where(
                    demanda.Demanda.responsavel
                    == db.get(usuario.Usuario, dados.get("responsavel_id"))
                )

            if dados.get("tipo_id"):
                consulta = consulta.where(
                    demanda.Demanda.responsavel
                    == db.get(demanda.TipoDemanda, dados.get("tipo_id"))
                )

            if dados.get("data_criacao"):
                consulta = consulta.where(
                    demanda.Demanda.data_criacao == dados.get("data_criacao")
                )

            demandas = db.execute(consulta).scalars().all()
            demandas_paginadas = servicos.paginar(demandas, 10)

            return renderizacao.renderizar_tabela_de_demandas(
                demandas=demandas_paginadas["paginador"](1),
                id_html="tabela-consulta-demanda",
                numero_paginas=demandas_paginadas["numero_paginas"],
                pagina_atual=1,
            )
        else:
            demandas = db.execute(consulta).scalars().all()[:10]

            return renderizacao.renderizar_tabela_de_demandas(
                demandas=demandas,
                id_html="tabela-consulta-demanda",
                numero_paginas=1,
                pagina_atual=1,
            )

    return app, db

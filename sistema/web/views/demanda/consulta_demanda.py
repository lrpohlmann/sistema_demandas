import flask
import sqlalchemy

from sistema.model.entidades import demanda, documento, fato, tarefa, usuario
from sistema import servicos
from sistema.web import renderizacao
from sistema.web.forms.consulta_demanda import criar_form, e_valido, obter_dados


def setup_views(app, db):
    @app.route("/demanda/consulta", methods=["GET"])
    def consulta_demanda():
        consulta = sqlalchemy.select(demanda.Demanda).order_by(
            demanda.Demanda.data_criacao
        )

        form_consulta_demanda = criar_form(
            [
                (r[0], r[1])
                for r in db.execute(
                    sqlalchemy.select(usuario.Usuario.id_usuario, usuario.Usuario.nome)
                ).fetchall()
            ],
            [
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
            if dados.get("titulo"):
                consulta = consulta.where(demanda.Demanda.titulo == dados.get("titulo"))

            if dados.get("responsavel_id"):
                consulta = consulta.where(
                    demanda.Demanda.responsavel_id == dados.get("responsavel_id")
                )

            if dados.get("tipo_id"):
                consulta = consulta.where(
                    demanda.Demanda.tipo_id == dados.get("tipo_id")
                )

            if dados.get("data_criacao"):
                consulta = consulta.where(
                    demanda.Demanda.data_criacao == dados.get("data_criacao")
                )

            demandas = db.execute(consulta).scalars().all()
            demandas_paginadas = servicos.paginar(demandas, 10)

            pagina_requerida = (
                int(flask.request.args.get("pagina"))
                if flask.request.args.get("pagina")
                else 1
            )
            return renderizacao.renderizar_tabela_de_demandas(
                demandas=demandas_paginadas["paginador"](pagina_requerida),
                id_html="tabela-consulta-demanda",
                numero_paginas=demandas_paginadas["numero_paginas"],
                pagina_atual=pagina_requerida,
            )
        else:
            return "", 400

    return app, db

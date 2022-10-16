from flask import request
from flask_login import login_required

from sistema.model.entidades import Demanda
from sistema import servicos
from sistema.web import renderizacao


def setup_views(app, db):
    @app.route("/demanda/ultimas-demandas-pendentes", methods=["GET"])
    @login_required
    def obter_ultimas_demandas_pendentes():
        consulta = db.query(Demanda)

        demandas = (
            consulta.filter(Demanda.status == "PENDENTE")
            .order_by(Demanda.data_criacao.desc())
            .all()
        )

        paginas = servicos.paginar(demandas, 10)

        pagina_requerida = (
            int(request.args.get("pagina")) if request.args.get("pagina") else 1
        )
        if pagina_requerida == 1 or (
            pagina_requerida < 1 or pagina_requerida > paginas["numero_paginas"]
        ):
            return renderizacao.renderizar_tabela_de_demandas(
                demandas=paginas["paginador"](1),
                numero_paginas=paginas["numero_paginas"],
                pagina_atual=1,
                nome_da_view="obter_ultimas_demandas_pendentes",
                kwargs_url={},
            )
        else:
            return renderizacao.renderizar_tabela_de_demandas(
                demandas=paginas["paginador"](pagina_requerida),
                numero_paginas=paginas["numero_paginas"],
                pagina_atual=pagina_requerida,
                nome_da_view="obter_ultimas_demandas_pendentes",
                kwargs_url={},
            )

    return app, db

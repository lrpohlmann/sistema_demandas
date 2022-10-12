from flask import render_template_string, request
import sqlalchemy
from flask_login import login_required

from sistema.model.entidades.fato import Fato
from ... import renderizacao
from sistema.servicos import pagincao


def setup_views(app, db):
    @app.route("/fato/card/lista/<int:demanda_id>", methods=["GET"])
    @login_required
    def lista_fato_card_view(demanda_id: int):
        fatos_paginados = pagincao.paginar(
            db.execute(sqlalchemy.select(Fato).where(Fato.demanda_id == demanda_id))
            .scalars()
            .all(),
            10,
        )

        numero_de_paginas = fatos_paginados["numero_paginas"]
        pagina_requerida = pagincao.validar_pagina_pedida(
            request.args.get("pagina"), numero_de_paginas
        )
        fatos_da_pagina_requerida = fatos_paginados["paginador"](pagina_requerida)

        return renderizacao.renderizar_lista_fato_card(
            fatos_da_pagina_requerida,
            pagina_requerida,
            numero_de_paginas,
            "lista_fato_card_view",
            {"demanda_id": demanda_id},
        )

    return app, db

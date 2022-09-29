from flask import render_template, request
from flask_login import login_required

from sistema.model.entidades.demanda import TipoDemanda


def setup_views(app, db):
    @app.route("/tipo_demanda", methods=["GET"])
    @login_required
    def tipo_demanda():
        tp_demanda = db.query(TipoDemanda).all()

        formato = request.args.get("formato")
        if request.method == "GET":
            if formato == "select":
                return render_template(
                    "componentes/option_tipo_demanda.html", tipo_demanda=tp_demanda
                )

    return app, db

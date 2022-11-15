from flask import redirect, render_template, request, url_for
import sqlalchemy
from flask_login import login_required

from sistema.model.entidades.demanda import Demanda, TipoDemanda
from sistema.model.entidades.usuario import Usuario
from sistema.web.forms.consulta_demanda_form import ConsultaDemandaForm
from sistema.web.forms import consulta_demanda_form, criar_demanda


def setup_views(app, db):
    @app.route("/", methods=["GET"])
    @login_required
    def main():
        return render_template(
            "home.html",
        )

    return app, db

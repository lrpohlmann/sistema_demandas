from urllib import request
import flask

from .. import renderizacao
from ..forms import login_form


def setup_views(app, db):
    @app.route("/login", methods=["GET", "POST"])
    def login():

        form = login_form.criar_form(**flask.request.form)
        if flask.request.method == "POST":
            if login_form.e_valido(form):
                pass

        return renderizacao.renderizar_pagina_login(form)

    return app, db

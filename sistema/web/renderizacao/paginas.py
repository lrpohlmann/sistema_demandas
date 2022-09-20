import flask


def renderizar_pagina_login(form_login) -> str:
    return flask.render_template("login.html", form_login=form_login)

import sqlalchemy
import flask
import flask_login

from .. import renderizacao
from ..forms import login_form, alterar_senha_form
from sistema.model.entidades.usuario import Usuario
from sistema.model.operacoes.usuario import confirmar_senha, definir_senha


def setup_views(app, db):
    @app.route("/login", methods=["GET", "POST"])
    def login():

        form = login_form.criar_form(**flask.request.form)
        if flask.request.method == "POST":
            if login_form.e_valido(form):
                dados_login = login_form.obter_dados(form)
                usuario = (
                    db.execute(
                        sqlalchemy.select(Usuario).where(
                            Usuario.nome == dados_login["nome"]
                        )
                    )
                    .scalars()
                    .one()
                )

                if usuario and confirmar_senha(usuario, dados_login["senha"]):
                    flask_login.login_user(usuario)
                    return flask.redirect("/")

        return renderizacao.renderizar_pagina_login(form)

    @app.route("/logout", methods=["GET", "POST"])
    @flask_login.login_required
    def logout():
        flask_login.logout_user()
        return flask.redirect(flask.url_for("login"))

    @app.route("/login/alterar-senha", methods=["GET", "POST"])
    @flask_login.login_required
    def alterar_senha_view():
        form = alterar_senha_form.criar_form(flask.request.form)
        if flask.request.method == "POST":
            if alterar_senha_form.e_valido(form):
                dados_form = alterar_senha_form.obter_dados(form)
                db.add(
                    definir_senha(flask_login.current_user, dados_form["nova_senha"])
                )
                db.commit()

                return flask.redirect("/", 200)
            else:
                return renderizacao.renderizar_pagina_alteracao_senha(form), 400

        return renderizacao.renderizar_pagina_alteracao_senha(form)

    return app, db

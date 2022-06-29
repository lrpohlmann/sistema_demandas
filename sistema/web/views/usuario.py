from flask import render_template
from sqlalchemy import select

from sistema.model.entidades.usuario import Usuario


def setup_views(app, db):
    @app.route("/usuario/formato/<tipo_formato>")
    def usuario(tipo_formato: str):
        if tipo_formato == "option":
            usuarios = db.execute(
                select(Usuario.id_usuario, Usuario.nome).order_by(Usuario.id_usuario)
            ).fetchall()
            return render_template("componentes/option_usuario.html", usuario=usuarios)

    return app, db

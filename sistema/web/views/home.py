from flask import render_template

from sistema.model.entidades.demanda import Demanda


def setup_views(app, db):
    @app.route("/")
    def main():
        demandas = db.query(Demanda).all()
        return render_template("home.html", demandas=demandas)

    return app, db

import flask
from flask_login import login_required


def setup_views(app, db):
    @app.route("/download_arquivo/<nome_arquivo>")
    @login_required
    def download_arquivo_view(nome_arquivo):
        return flask.send_from_directory(app.config["UPLOAD_FOLDER"], nome_arquivo)

    return app, db

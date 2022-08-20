import flask


def setup_views(app, db):
    @app.route("/download_arquivo/<nome_arquivo>")
    def download_arquivo_view(nome_arquivo):
        return flask.send_from_directory(app.config["UPLOAD_FOLDER"], nome_arquivo)

    return app, db

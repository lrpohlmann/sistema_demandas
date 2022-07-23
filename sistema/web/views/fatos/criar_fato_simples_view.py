def setup_views(app, db):
    @app.route("/fato/criar/simples", methods=["POST"])
    def criar_fato_simples_view():
        return "", 500

    return app, db

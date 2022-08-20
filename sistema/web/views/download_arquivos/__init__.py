from sistema.web.views.download_arquivos import download_arquivos_view


def setup_views(app, db):
    for v in [
        download_arquivos_view,
    ]:
        v.setup_views(app, db)

    return app, db

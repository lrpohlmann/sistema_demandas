from . import obter_lista_de_documentos


def setup_views(app, db):
    for v in [obter_lista_de_documentos]:
        app, db = v.setup_views(app, db)

    return app, db

from . import obter_lista_de_documentos, tipo_documento_view, inserir_documento_view


def setup_views(app, db):
    for v in [obter_lista_de_documentos, tipo_documento_view, inserir_documento_view]:
        app, db = v.setup_views(app, db)

    return app, db

from sistema.web.views.fatos import criar_fato_simples_view, lista_fato_card_view


def setup_views(app, db):
    for v in [criar_fato_simples_view, lista_fato_card_view]:
        v.setup_views(app, db)

    return app, db

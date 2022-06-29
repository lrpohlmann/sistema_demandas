from datetime import datetime
from typing import Mapping, Optional, Sequence
from flask import Flask, render_template, request
from sqlalchemy import select
from sqlalchemy.orm import scoped_session
from sqlalchemy.exc import NoResultFound
from pathlib import Path

from sistema.model.entidades.demanda import Demanda, TipoDemanda
from sistema.model.entidades.usuario import Usuario
from sistema.persistencia import setup_persistencia
from sistema.web.forms.consulta_demanda import ConsultaDemandaForm
from sistema.web.forms.criar_demanda import CriarDemandaForm
from sistema.web.views import setup_todas_views


CONFIG_TEST_FILE = Path(__file__).parent / "configs" / "config_teste.py"


def criar_web_app(test_config=None) -> Flask:
    app = _setup_web_app(test_config)
    db, mapper, metadata = _setup_app_db(app)
    setup_todas_views(app, db)
    return app


def _setup_web_app(test_config=False, mapping_config: Optional[Mapping] = None):
    app = Flask(__name__)
    if test_config:
        app.config.from_pyfile(str(CONFIG_TEST_FILE))
    else:
        pass

    if mapping_config:
        app.config.from_mapping(mapping_config)

    return app


def _setup_app_db(app: Flask):
    db, mapper, metadata = setup_persistencia(app.config["DB"])

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db.remove()

    return db, mapper, metadata

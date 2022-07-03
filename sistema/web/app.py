from datetime import datetime
from typing import Mapping, Optional, Sequence
from flask import Flask
from flask_wtf.csrf import CSRFProtect
from pathlib import Path

from sistema.persistencia import setup_persistencia
from sistema.web.views import setup_todas_views


CONFIG_TEST_FILE = Path(__file__).parent / "configs" / "config_teste.py"


def criar_web_app(test_config=None, mapping_config: Optional[Mapping] = None) -> Flask:
    app = _setup_web_app(test_config, mapping_config)
    db, mapper, metadata = _setup_app_db(app)
    setup_todas_views(app, db)
    return app


def _setup_web_app(test_config=False, mapping_config: Optional[Mapping] = None):
    app = Flask(__name__)
    CSRFProtect(app)

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

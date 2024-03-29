import logging
from dataclasses import dataclass
from typing import Mapping, Optional, Sequence
from flask import Flask
from flask.cli import load_dotenv
from dotenv import dotenv_values
from flask_wtf.csrf import CSRFProtect
from pathlib import Path
import flask_login
from sqlalchemy.orm import scoped_session, registry
from sqlalchemy import MetaData

from sistema.model.entidades.usuario import Usuario
from sistema.persistencia import setup_persistencia
from sistema.web.views import setup_todas_views
from sistema.web import autenticacao

CONFIG_TEST_FILE = Path(__file__).parent / "configs" / "config_teste.py"


@dataclass
class ContextoDb:
    db: scoped_session
    mapper: registry
    metadata: MetaData


@dataclass
class WebAppContextoRuntime:
    app: Flask
    persistencia: ContextoDb


def web_app_factory(
    config_obj, mapping_config: Optional[Mapping] = None
) -> WebAppContextoRuntime:
    app = _setup_web_app(config_obj, mapping_config)
    db = _setup_app_db(app)
    web_app_contexto = WebAppContextoRuntime(app=app, persistencia=db)

    _setup_app_autenticacao(web_app_contexto.app, web_app_contexto.persistencia.db)
    setup_todas_views(web_app_contexto.app, web_app_contexto.persistencia.db)

    return web_app_contexto


def web_app_producao_factory() -> Flask:
    logging.basicConfig(filename="sistema_log.log", level=logging.ERROR)
    app = Flask(__name__)
    CSRFProtect(app)
    load_dotenv()
    app.config["SECRET_KEY"] = dotenv_values()["SECRET_KEY"]
    app.config["UPLOAD_FOLDER"] = str(Path(dotenv_values()["UPLOAD_FOLDER"]).absolute())
    contexto_db = _setup_app_db(app, dotenv_values()["DB"])
    _setup_app_autenticacao(app, contexto_db.db)
    setup_todas_views(app, contexto_db.db)
    return app


def _setup_web_app(config_obj, mapping_config: Optional[Mapping] = None):
    app = Flask(__name__)
    CSRFProtect(app)

    app.config.from_object(config_obj)

    if mapping_config:
        app.config.from_mapping(mapping_config)

    return app


def _setup_app_db(app: Flask, db_url: Optional[str] = None) -> ContextoDb:
    if not db_url:
        contexto_db = ContextoDb(*setup_persistencia(app.config["DB"]))
    else:
        contexto_db = ContextoDb(*setup_persistencia(db_url))

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        contexto_db.db.remove()

    return contexto_db


def _setup_app_autenticacao(app, db):
    login_manager = flask_login.LoginManager()
    login_manager.login_view = "/login"
    login_manager.init_app(app)

    autenticacao.carregar_usuario_factory(
        login_manager,
        lambda id_usuario: db.get(Usuario, int(id_usuario)),
    )

    return app, db

from functools import reduce
from re import U
from typing import Tuple
from flask import Flask
from sqlalchemy.orm import scoped_session

from sistema.web.views import (
    demanda,
    home,
    tarefa,
    fatos,
    download_arquivos,
    login,
    documento,
)


def setup_todas_views(app: Flask, db: scoped_session) -> Tuple[Flask, scoped_session]:
    return reduce(
        lambda args, setup_views: setup_views(*args),
        [
            demanda.setup_views,
            home.setup_views,
            tarefa.setup_views,
            fatos.setup_views,
            download_arquivos.setup_views,
            login.setup_views,
            documento.setup_views,
        ],
        (app, db),
    )

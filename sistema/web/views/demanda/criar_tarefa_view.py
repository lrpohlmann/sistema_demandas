from flask import request
from flask_login import login_required

from sistema.model.entidades.demanda import Demanda
from sistema.model.entidades.tarefa import Tarefa
from sistema.model.entidades.usuario import Usuario
from sistema.web import renderizacao
from sistema.web.forms import criar_tarefa
from sistema.web import eventos_cliente


def setup_views(app, db):

    return app, db

from typing import Sequence
from flask_wtf import FlaskForm
from wtforms import StringField, DateTimeField, SelectField


class ConsultaDemandaForm(FlaskForm):
    titulo = StringField("Título")
    responsavel_id = SelectField("Responsável", coerce=lambda x: int(x) if x else None)
    tipo_id = SelectField("Tipo", coerce=lambda x: int(x) if x else None)
    data_criacao = DateTimeField("Data de Criação")


def criar_form(
    opcoes_responsavel_id: Sequence, opcoes_tipo_id: Sequence, **dados
) -> ConsultaDemandaForm:
    form = ConsultaDemandaForm(**dados)
    form.responsavel_id.choices = opcoes_responsavel_id
    form.tipo_id.choices = opcoes_tipo_id
    return form

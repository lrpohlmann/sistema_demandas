from typing import Mapping
from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, TextAreaField, HiddenField, validators


class CriarFatoSimplesForm(FlaskForm):
    demanda_id = HiddenField(validators=[validators.DataRequired()], filters=[int])
    titulo = StringField("Título", validators=[validators.DataRequired()])
    descricao = TextAreaField(label="Descrição")


def criar_form(**dados) -> CriarFatoSimplesForm:
    form = CriarFatoSimplesForm(**dados)
    return form


def e_valido(form) -> bool:
    return form.validate()


def obter_dados(form) -> Mapping:
    dados = dict(form.data)
    return dados

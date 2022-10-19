from typing import Mapping
from flask_wtf import FlaskForm
from wtforms import StringField, validators


class CriarTipoDemandaForm(FlaskForm):
    nome = StringField(
        "Nome do Tipo de Demanda",
        validators=[validators.InputRequired("Campo Necessário.")],
    )


def criar_form(dados_input_usuario=None, **dados) -> CriarTipoDemandaForm:
    return CriarTipoDemandaForm(formdata=dados_input_usuario, **dados)


def e_valido(form) -> bool:
    return form.validate()


def obter_dados(form) -> Mapping:
    dados = dict(form.data)
    return dados

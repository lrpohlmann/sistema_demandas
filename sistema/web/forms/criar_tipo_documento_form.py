from typing import Mapping
from flask_wtf import FlaskForm
from wtforms import StringField, validators


class CriarTipoDocumentoForm(FlaskForm):
    nome = StringField(
        "Nome", validators=[validators.InputRequired("Campo necessário.")]
    )


def criar_form(dados_input_usuario=None, **dados) -> CriarTipoDocumentoForm:
    return CriarTipoDocumentoForm(formdata=dados_input_usuario, **dados)


def e_valido(form) -> bool:
    return form.validate()


def obter_dados(form) -> Mapping:
    dados = dict(form.data)
    return dados

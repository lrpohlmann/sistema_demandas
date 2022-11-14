from typing import Mapping, Callable
from flask_wtf import FlaskForm
from wtforms import StringField, validators, Field


class CriarTipoDocumentoForm(FlaskForm):
    nome = StringField(
        "Nome", validators=[validators.InputRequired("Campo necessário.")]
    )


def criar_form(dados_input_usuario=None, **dados) -> CriarTipoDocumentoForm:
    return CriarTipoDocumentoForm(formdata=dados_input_usuario, **dados)


def e_valido(
    form: FlaskForm, validador_nome_unico: Callable[[FlaskForm, Field], None]
) -> bool:
    return form.validate(extra_validators={"nome": [validador_nome_unico]})


def obter_dados(form) -> Mapping:
    dados = dict(form.data)
    return dados

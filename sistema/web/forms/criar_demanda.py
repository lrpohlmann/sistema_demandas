from datetime import datetime
from typing import Mapping
from flask_wtf import FlaskForm
from wtforms import StringField, DateTimeField, SelectField, validators


class CriarDemandaForm(FlaskForm):
    titulo = StringField(
        "Título",
        validators=[validators.DataRequired("Campo necessário")],
    )
    tipo_id = SelectField(label="Tipo", coerce=lambda x: int(x) if x else None)
    responsavel_id = SelectField(
        label="Responsável", coerce=lambda x: int(x) if x else None
    )
    data_entrega = DateTimeField("Data de Entrega", format=["", "%Y-%m-%d %H:%M:%S"])


def criar_form(tipo_id_escolhas, responsavel_id_escolhas, **dados):
    f = CriarDemandaForm(**dados)
    f.responsavel_id.choices = responsavel_id_escolhas
    f.tipo_id.choices = tipo_id_escolhas
    return f


def e_valido(form) -> bool:
    return form.validate()


def obter_dados(form) -> Mapping:
    dados = dict(dados.data)
    if dados["data_entrega"] == datetime(1900, 1, 1, 0, 0):
        dados["data_entrega"] = None

    return dados

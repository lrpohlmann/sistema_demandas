from datetime import datetime
from typing import Any, Mapping, Sequence, Tuple
from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, DateTimeField, TextAreaField, validators


class CriarTarefaForm(FlaskForm):
    titulo = StringField(
        "título", validators=[validators.DataRequired("Campo necessário.")]
    )
    responsavel_id = SelectField("Responsável", coerce=lambda x: int(x) if x else None)
    data_entrega = DateTimeField(
        "Data de Entrega",
        format=["%Y-%m-%d %H:%M:%S", ""],
        filters=[
            lambda x: x if x else None,
        ],
    )
    descricao = TextAreaField("Descrição")


def criar_form(
    escolhas_responsavel: Sequence[Tuple[int, Any]], **dados
) -> CriarTarefaForm:
    form = CriarTarefaForm(**dados)
    form.responsavel_id.choices = escolhas_responsavel
    return form


def e_valido(form, **kwargs) -> bool:
    return form.validate(**kwargs)


def obter_dados(form) -> Mapping:
    dados = dict(form.data)
    if dados["data_entrega"] == datetime(1900, 1, 1, 0, 0):
        dados["data_entrega"] = None

    return dados

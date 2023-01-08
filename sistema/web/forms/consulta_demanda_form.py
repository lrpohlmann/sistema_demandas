from datetime import datetime
from typing import Mapping, Sequence
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, validators

from sistema.web.forms.campos import DateFieldSemValidacaoFormato


class ConsultaDemandaForm(FlaskForm):
    titulo = StringField("Título", validators=[validators.Optional()])
    responsavel_id = SelectField(
        "Responsável",
        coerce=lambda x: int(x) if x else None,
        validators=[validators.Optional()],
    )
    tipo_id = SelectField(
        "Tipo",
        coerce=lambda x: int(x) if x else None,
        validators=[validators.Optional()],
    )

    periodo_data_criacao_inicio = DateFieldSemValidacaoFormato(
        "Início", validators=[validators.Optional()]
    )
    periodo_data_criacao_fim = DateFieldSemValidacaoFormato(
        "Fim", validators=[validators.Optional()]
    )

    periodo_data_entrega_inicio = DateFieldSemValidacaoFormato(
        "Início", validators=[validators.Optional()]
    )
    periodo_data_entrega_fim = DateFieldSemValidacaoFormato(
        "Fim", validators=[validators.Optional()]
    )

    status = SelectField(
        "Status",
        validators=[validators.Optional()],
        choices=[
            ("", "(Qualquer Status)"),
            ("PENDENTE", "Pendente"),
            ("RESOLVIDO", "Resolvido"),
        ],
    )


def criar_form(
    opcoes_responsavel_id: Sequence, opcoes_tipo_id: Sequence, input_usuario=None,**dados
) -> ConsultaDemandaForm:
    form = ConsultaDemandaForm(formdata=input_usuario, **dados)
    form.responsavel_id.choices = opcoes_responsavel_id
    form.tipo_id.choices = opcoes_tipo_id
    return form


def e_valido(form) -> bool:
    return form.validate()


def obter_dados(form) -> Mapping:
    dados = dict(form.data)
    return dados

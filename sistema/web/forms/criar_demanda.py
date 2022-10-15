from datetime import datetime
from typing import Mapping
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SelectField,
    validators,
    DateField,
    TimeField,
    ValidationError,
)


class DateFieldSemValidacaoFormato(DateField):
    def process_formdata(self, valuelist):
        if isinstance(valuelist[0], str):
            self.data = valuelist[0]
            return
        else:
            self.data = None
            return


class TimeFieldSemValidacaoFormato(TimeField):
    def process_formdata(self, valuelist):
        if isinstance(valuelist[0], str):
            self.data = valuelist[0]
            return
        else:
            self.data = None
            return


def _checar_se_dia_e_hora_estao_preenchidos(form, field):
    if bool(form.data["dia_entrega"]) ^ bool(form.data["hora_entrega"]):  # xor
        raise ValidationError("Dia e Hora devem ser preenchidos conjuntamente.")


def _factory_validador_de_formato_data_e_tempo(formato, extrair_valor_func):
    def _validar_formato_data_e_tempo(form, field):
        if field.data:
            try:
                valor = extrair_valor_func(datetime.strptime(field.data, formato))
                field.data = valor
            except ValueError:
                raise ValidationError("Formato de data não suportado")

    return _validar_formato_data_e_tempo


class CriarDemandaForm(FlaskForm):
    titulo = StringField(
        "Título",
        validators=[validators.InputRequired("Campo necessário")],
    )
    tipo_id = SelectField(label="Tipo", coerce=lambda x: int(x) if x else None)
    responsavel_id = SelectField(
        label="Responsável", coerce=lambda x: int(x) if x else None
    )
    dia_entrega = DateFieldSemValidacaoFormato(
        "Dia de Entrega",
        validators=[
            _checar_se_dia_e_hora_estao_preenchidos,
            _factory_validador_de_formato_data_e_tempo("%Y-%m-%d", lambda x: x.date()),
        ],
    )
    hora_entrega = TimeFieldSemValidacaoFormato(
        "Hora de Entrega",
        validators=[
            _checar_se_dia_e_hora_estao_preenchidos,
            _factory_validador_de_formato_data_e_tempo("%H:%M", lambda x: x.time()),
        ],
    )


def criar_form(
    tipo_id_escolhas, responsavel_id_escolhas, dados_input_usuario=None, **dados
):
    f = CriarDemandaForm(formdata=dados_input_usuario, **dados)
    f.responsavel_id.choices = responsavel_id_escolhas
    f.tipo_id.choices = tipo_id_escolhas
    return f


def e_valido(form) -> bool:
    return form.validate()


def obter_dados(form: CriarDemandaForm) -> Mapping:
    dados = dict(form.data)
    dia_entrega = dados.pop("dia_entrega")
    hora_entrega = dados.pop("hora_entrega")

    if dia_entrega and hora_entrega:
        dados["data_entrega"] = datetime.combine(dia_entrega, hora_entrega)

    return dados

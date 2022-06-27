from flask_wtf import FlaskForm
from wtforms import StringField, DateTimeField, SelectField


class ConsultaDemandaForm(FlaskForm):
    titulo = StringField("Título")
    responsavel_id = SelectField("Responsável", coerce=lambda x: int(x) if x else None)
    tipo_id = SelectField("Tipo", coerce=lambda x: int(x) if x else None)
    data_criacao = DateTimeField("Data de Criação")

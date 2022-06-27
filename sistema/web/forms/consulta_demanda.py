from flask_wtf import FlaskForm
from wtforms import StringField, DateTimeField, SelectField


class ConsultaDemandaForm(FlaskForm):
    titulo = StringField("Título")
    responsavel_id = SelectField("Responsável")
    tipo_id = SelectField("Tipo")
    data_criacao = DateTimeField("Data de Criação")

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


def criar_form(tipo_id_escolhas, responsavel_id_escolhas, **dados):
    f = CriarDemandaForm(**dados)
    f.responsavel_id.choices = responsavel_id_escolhas
    f.tipo_id.choices = tipo_id_escolhas
    return f

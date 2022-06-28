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
    data_entrega = DateTimeField("Data de Entrega")

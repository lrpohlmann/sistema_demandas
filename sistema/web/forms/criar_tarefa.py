from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, DateTimeField, TextAreaField, validators


class CriarTarefaForm(FlaskForm):
    titulo = StringField(
        "título", validators=[validators.DataRequired("Campo necessário.")]
    )
    responsavel_id = SelectField("Responsável", coerce=lambda x: int(x) if x else None)
    data_entrega = DateTimeField("Data de Entrega")
    descricao = TextAreaField("Descrição")

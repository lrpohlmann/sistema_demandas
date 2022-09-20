from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SelectField, validators


class EditarDadosDemandaForm(FlaskForm):
    responsavel_id = SelectField("Responsável", coerce=lambda x: int(x) if x else None)
    tipo_id = SelectField("Tipo", coerce=int, validators=[validators.InputRequired()])
    status = SelectField("Status")


def criar_form(
    escolhas_responsavel, escolhas_tipo, escolhas_status, **dados
) -> EditarDadosDemandaForm:
    form = EditarDadosDemandaForm(**dados)
    form.responsavel_id.choices = escolhas_responsavel
    form.tipo_id.choices = escolhas_tipo
    form.status.choices = escolhas_status
    return form

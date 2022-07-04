from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SelectField, validators


class EditarDadosDemandaForm(FlaskForm):
    responsavel_id = SelectField("Responsável", coerce=lambda x: int(x) if x else None)
    tipo_id = SelectField("Tipo", coerce=int, validators=[validators.InputRequired()])
    documentos = FileField(
        "Documentos",
        validators=[
            FileAllowed(
                [
                    "pdf",
                    "doc",
                    "docx",
                    "xls",
                    "xlsx",
                    "shp",
                    "shx",
                    "dbf",
                    "cpg",
                    "prj",
                    "rar",
                    "zip",
                ],
                "Extensão inválida.",
            )
        ],
    )


def criar_form(escolhas_responsavel, escolhas_tipo, **dados) -> EditarDadosDemandaForm:
    form = EditarDadosDemandaForm(**dados)
    form.responsavel_id.choices = escolhas_responsavel
    form.tipo_id.choices = escolhas_tipo
    return form

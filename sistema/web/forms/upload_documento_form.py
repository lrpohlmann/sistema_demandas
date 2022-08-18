from typing import Dict, Mapping, Sequence
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, SelectField, TextAreaField, validators


class UploadDocumentoForm(FlaskForm):
    nome = StringField(
        "Nome",
        validators=[
            validators.DataRequired(),
        ],
    )
    tipo = SelectField(
        "Tipo",
        coerce=int,
        validators=[
            validators.DataRequired(),
        ],
    )
    identificador = StringField("Identificador")
    descricao = TextAreaField("Descrição")
    arquivo = FileField(
        "Arquivo",
        validators=[
            FileRequired("Arquivo Necessário"),
            FileAllowed(
                {
                    "jpg",
                    "png",
                    "pdf",
                    "xlsx",
                    "xls",
                    "ods",
                    "docx",
                    "doc",
                    "odt",
                    "rar",
                    "7z",
                    "zip",
                }
            ),
        ],
    )


def criar_form(escolhas_tipo_documento: Sequence, **dados) -> UploadDocumentoForm:
    form = UploadDocumentoForm(**dados)
    form.tipo.choices = escolhas_tipo_documento
    return form


def e_valido(form) -> bool:
    return form.validate()


def obter_dados(form) -> Dict:
    dados = dict(form.data)
    return dados

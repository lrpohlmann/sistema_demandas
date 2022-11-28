from typing import Dict, Mapping, Sequence
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired, FileSize
from wtforms import StringField, SelectField, TextAreaField, validators

from sistema.web.configs import constantes


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
            FileSize(
                max_size=constantes.TAMANHO_MAXIMO_ARQUIVOS,
                message="Arquivo não pode ser maior do que 20 megabytes",
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

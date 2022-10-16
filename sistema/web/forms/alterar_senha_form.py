from typing import Mapping
from flask_wtf import FlaskForm
from wtforms import PasswordField, validators, ValidationError


def _validar_se_campos_de_senha_tem_o_mesmo_valor(form, field):
    if not form.data["nova_senha"] == form.data["nova_senha_repeticao"]:
        raise ValidationError("As senhas estão diferentes entre os campos.")


class AlterarSenhaForm(FlaskForm):
    nova_senha = PasswordField(
        "Nova Senha",
        validators=[
            validators.InputRequired("Campo necessário."),
            _validar_se_campos_de_senha_tem_o_mesmo_valor,
        ],
    )
    nova_senha_repeticao = PasswordField(
        "Nova Senha Novamente",
        validators=[
            validators.InputRequired("Campo necessário."),
            _validar_se_campos_de_senha_tem_o_mesmo_valor,
        ],
    )


def criar_form(dados_input_usuario=None, **dados):
    return AlterarSenhaForm(formdata=dados_input_usuario, **dados)


def e_valido(form):
    return form.validate()


def obter_dados(form) -> Mapping:
    return dict(form.data)

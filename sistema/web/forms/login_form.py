from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, validators


class LoginForm(FlaskForm):
    nome = StringField(
        "Nome", validators=[validators.DataRequired("Campo necessário.")]
    )
    senha = PasswordField(
        "Senha", validators=[validators.DataRequired("Campo necessário.")]
    )


def criar_form(**dados):
    return LoginForm(**dados)


def e_valido(form) -> bool:
    return form.validate()


def obter_dados(form):
    return dict(form.data)

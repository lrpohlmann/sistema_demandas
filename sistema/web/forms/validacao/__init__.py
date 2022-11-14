from wtforms import ValidationError, Field
from flask_wtf import FlaskForm

from typing import Callable, Any


def validador_campo_unico_factory(
    funcao_teste_existencia: Callable[[Any], bool], mensagem: str = "Valor já existe."
) -> Callable[[FlaskForm, Field], None]:
    def _validador(form: FlaskForm, field: Field):
        if funcao_teste_existencia(field.data):
            raise ValidationError(mensagem)

    return _validador

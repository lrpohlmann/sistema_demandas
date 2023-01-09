from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import validators
from werkzeug.datastructures import MultiDict

from test.test_web.fixtures import web_app_com_autenticacao, WebAppFixture
from sistema.web.forms.campos import (
    DateFieldSemValidacaoFormato,
)


def test_date_field_sem_validacao_formato(web_app_com_autenticacao: WebAppFixture):
    class FormTest(FlaskForm):
        campo = DateFieldSemValidacaoFormato("hm")

    with web_app_com_autenticacao.app.app_context():
        form = FormTest(formdata=MultiDict({"campo": "2022-01-01"}))

        assert form.validate()

        dados = form.data
        assert dados["campo"]

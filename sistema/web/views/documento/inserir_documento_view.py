from flask import request, render_template_string, abort
import sqlalchemy
from flask_login import login_required

from sistema.web import renderizacao, upload_arquivo
from sistema.web.forms import upload_documento_form
from sistema.model.entidades.demanda import Demanda
from sistema.model.entidades.documento import TipoDocumento, Documento
from sistema.web import eventos_cliente


def setup_views(app, db):
    @app.route("/documento/form/criar/<int:demanda_id>", methods=["GET"])
    @login_required
    def obter_form_inserir_documento_view(demanda_id: int):
        escolhas = [
            list(x)
            for x in db.execute(
                sqlalchemy.select(TipoDocumento.id_tipo_documento, TipoDocumento.nome)
            )
        ]

        return renderizacao.renderizar_inserir_documento_form(
            upload_documento_form.criar_form(
                escolhas_tipo_documento=escolhas,
            ),
            demanda_id,
        )

    @app.route("/documento/criar/<int:demanda_id>", methods=["POST"])
    @login_required
    def inserir_documento_view(demanda_id: int):
        demanda: Demanda = db.get(Demanda, demanda_id)
        if not demanda:
            return abort(404)

        escolhas = [
            list(x)
            for x in db.execute(
                sqlalchemy.select(TipoDocumento.id_tipo_documento, TipoDocumento.nome)
            )
        ]

        form = upload_documento_form.criar_form(
            escolhas, arquivo=request.files["arquivo"], **request.form
        )

        form_e_valido = upload_documento_form.e_valido(form)
        if form_e_valido:
            dado = upload_documento_form.obter_dados(form)
            caminho = upload_arquivo.salvar(
                app.config["UPLOAD_FOLDER"],
                dado["arquivo"],
            )

            demanda.documentos.append(
                Documento(
                    nome=dado["nome"],
                    tipo=db.get(TipoDocumento, dado["tipo"]),
                    identificador=dado["identificador"],
                    descricao=dado["descricao"],
                    arquivo=caminho,
                )
            )
            db.add(demanda)
            db.commit()

            return (
                renderizacao.renderizar_inserir_documento_form(
                    form,
                    demanda_id,
                ),
                201,
                {"HX-Trigger": eventos_cliente.DOCUMENTO_CRIADO},
            )
        else:
            return (
                renderizacao.renderizar_inserir_documento_form(
                    form,
                    demanda_id,
                ),
                200,
            )

    return app, db

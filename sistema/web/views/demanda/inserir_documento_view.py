from flask import request, render_template_string
import sqlalchemy
from flask_login import login_required

from sistema.web import renderizacao, upload_arquivo
from sistema.web.forms import upload_documento_form
from sistema.model.entidades.demanda import Demanda
from sistema.model.entidades.documento import TipoDocumento, Documento


def setup_views(app, db):
    @app.route(
        "/demanda/editar/inserir_documento/<int:demanda_id>", methods=["GET", "POST"]
    )
    @login_required
    def inserir_documento_view(demanda_id: int):
        demanda = db.get(Demanda, demanda_id)

        escolhas = [
            list(x)
            for x in db.execute(
                sqlalchemy.select(TipoDocumento.id_tipo_documento, TipoDocumento.nome)
            )
        ]
        if request.method == "GET":
            return renderizacao.renderizar_inserir_documento_form(
                upload_documento_form.criar_form(
                    escolhas_tipo_documento=escolhas,
                ),
                demanda_id,
            )

        elif request.method == "POST":
            form = upload_documento_form.criar_form(
                escolhas, arquivo=request.files["arquivo"], **request.form
            )
            if upload_documento_form.e_valido(form):
                dado = upload_documento_form.obter_dados(form)
                caminho = upload_arquivo.salvar(app, dado["arquivo"])

                demanda.documentos.append(
                    Documento(
                        nome=dado.get("nome"),
                        tipo=db.get(TipoDocumento, dado.get("tipo")),
                        identificador=dado.get("identificador"),
                        descricao=dado.get("descricao"),
                        arquivo=caminho,
                    )
                )
                db.add(demanda)
                db.commit()

                return (
                    renderizacao.renderizar_inserir_documento_form(
                        upload_documento_form.criar_form(
                            escolhas_tipo_documento=escolhas,
                        ),
                        demanda_id,
                    ),
                    201,
                )
            else:
                return (
                    renderizacao.renderizar_inserir_documento_form(
                        upload_documento_form.criar_form(
                            escolhas_tipo_documento=escolhas,
                        ),
                        demanda_id,
                    ),
                    200,
                )

    return app, db

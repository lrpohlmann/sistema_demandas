from telnetlib import DO
from sqlalchemy import (
    create_engine,
    Table,
    MetaData,
    String,
    Integer,
    Column,
    ForeignKey,
    insert,
    select,
)
from sqlalchemy.engine import Engine
import pytest

from sistema.model.entidades.documento import Documento, TipoDocumento


@pytest.fixture
def _engine():
    return create_engine("sqlite+pysqlite:///:memory:", echo=True, future=True)


def test_inserir_documento(_engine: Engine):
    metadata = MetaData(bind=_engine)

    tipo_documento_tabela = Table(
        "tipo_documento",
        metadata,
        Column("id_tipo_documento", Integer, primary_key=True),
        Column("nome", String, nullable=False),
    )

    documento_tabela = Table(
        "documento",
        metadata,
        Column("id_documento", Integer, primary_key=True),
        Column("identificador", String, unique=True),
        Column("tipo", ForeignKey("tipo_documento.id_tipo_documento"), nullable=False),
        Column("nome", String, nullable=False),
        Column("descricao", String),
        Column("arquivo", String),
    )

    metadata.create_all()

    def inserir_tipo_documento(tipo: TipoDocumento):
        with _engine.begin() as conn:
            query = insert(tipo_documento_tabela).values(nome=tipo.nome)
            conn.execute(query)

    def inserir_documento(documento: Documento):
        campos_normais = dict([(k, v) for k, v in documento.iteritems() if k != "tipo"])
        with _engine.begin() as conn:
            query = insert(documento_tabela).values(
                tipo=documento.tipo.id_tipo_documento, **campos_normais
            )
            conn.execute(query)

    tp_doc = TipoDocumento(id_tipo_documento=1, nome="Processo")
    documento = Documento(tipo=tp_doc, nome="221188")

    inserir_tipo_documento(tp_doc)

    inserir_documento(documento)

    with _engine.begin() as conn:
        query = select(documento_tabela)
        res = conn.execute(query)

    doc_salvo = res.fetchone()
    dict_doc_salvo = doc_salvo._mapping
    for k, v in documento.items():
        if k == "id_documento":
            assert dict_doc_salvo[k] == 1
        elif k == "tipo":
            assert dict_doc_salvo[k] == v.id_tipo_documento
        else:
            assert dict_doc_salvo[k] == v

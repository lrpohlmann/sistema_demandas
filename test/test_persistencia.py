from telnetlib import DO
from typing import Mapping
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
from sqlalchemy import event

import pytest

from sistema.model.entidades.documento import Documento, TipoDocumento


def init_tabela_tipo_document(metadata):
    return Table(
        "tipo_documento",
        metadata,
        Column("id_tipo_documento", Integer, primary_key=True),
        Column("nome", String, nullable=False),
    )


def init_tabela_documento(metadata):
    return Table(
        "documento",
        metadata,
        Column("id_documento", Integer, primary_key=True),
        Column("identificador", String, unique=True),
        Column("tipo", ForeignKey("tipo_documento.id_tipo_documento"), nullable=False),
        Column("nome", String, nullable=False),
        Column("descricao", String),
        Column("arquivo", String),
    )


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


@pytest.fixture
def _engine():
    return create_engine("sqlite+pysqlite:///:memory:", echo=True, future=True)


@pytest.fixture
def _metadata():
    return MetaData()


def test_inserir_documento(_engine, _metadata):

    tipo_documento_tabela = init_tabela_tipo_document(_metadata)

    documento_tabela = init_tabela_documento(_metadata)

    _metadata.create_all(bind=_engine)

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


def test_obter_documento_do_db(_engine, _metadata):
    tipo_documento_tabela = init_tabela_tipo_document(_metadata)

    documento_tabela = init_tabela_documento(_metadata)

    _metadata.create_all(bind=_engine)

    with _engine.begin() as conn:
        conn.execute(insert(tipo_documento_tabela).values([{"nome": "PROCESSO"}]))
        conn.execute(
            insert(documento_tabela).values([{"tipo": 1, "nome": "Processo12-05-2022"}])
        )

    with _engine.begin() as conn:
        doc_db = conn.execute(select(documento_tabela)).fetchone()
        tipo_doc_db = conn.execute(
            select(tipo_documento_tabela).filter(
                tipo_documento_tabela.c.id_tipo_documento == doc_db["tipo"]
            )
        ).fetchone()

    dados_db = dict(**doc_db._mapping)
    dados_db["tipo"] = dict(**tipo_doc_db._mapping)

    def reconstituir_documento(dados_db: Mapping) -> Documento:
        return Documento(
            id_documento=dados_db["id_documento"],
            identificador=dados_db["identificador"],
            tipo=TipoDocumento(**dados_db["tipo"]),
            nome=dados_db["nome"],
            descricao=dados_db["descricao"],
            arquivo=dados_db["arquivo"],
        )

    documento_reconstituido = reconstituir_documento(dados_db)
    assert isinstance(documento_reconstituido, Documento)

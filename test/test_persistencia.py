from pydoc import doc
from tkinter import N
from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    MetaData,
    String,
    Table,
    event,
    DateTime,
    create_engine,
    JSON,
)
from sqlalchemy.orm import registry, relationship, Session
from sqlalchemy.engine import Engine
import pytest
from sistema.model.entidades.demanda import Demanda, TipoDemanda

from sistema.model.entidades.documento import TipoDocumento, Documento
from sistema.model.entidades.fato import Fato, TipoFatos
from sistema.model.entidades.tarefa import Tarefa
from sistema.model.entidades.usuario import Usuario


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


def init_tabela_tipo_documento(metadata):
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
        Column("identificador", String, nullable=True),
        Column(
            "tipo_id", ForeignKey("tipo_documento.id_tipo_documento"), nullable=False
        ),
        Column("descricao", String, nullable=True),
        Column("arquivo", String, nullable=True),
        Column("demanda_id", ForeignKey("demanda.id_demanda")),
    )


def init_tabela_usuario(metadata):
    return Table(
        "usuario",
        metadata,
        Column("id_usuario", Integer, primary_key=True),
        Column("nome", String, nullable=False),
        Column("senha", String, nullable=False),
    )


def init_tabela_tipo_demanda(metadata):
    return Table(
        "tipo_demanda",
        metadata,
        Column("id_tipo_demanda", Integer, primary_key=True),
        Column("nome", String, nullable=False),
    )


def init_tabela_demanda(metadata):
    return Table(
        "demanda",
        metadata,
        Column("id_demanda", Integer, primary_key=True),
        Column("titulo", String, nullable=True),
        Column("tipo_id", ForeignKey("tipo_demanda.id_tipo_demanda"), nullable=False),
        Column("responsavel_id", ForeignKey("usuario.id_usuario"), nullable=True),
        Column("data_criacao", DateTime, nullable=False),
        Column("data_entrega", DateTime, nullable=True),
    )


def init_tabela_tarefa(metadata):
    return Table(
        "tarefa",
        metadata,
        Column("id_tarefa", Integer, primary_key=True),
        Column("titulo", String, nullable=False),
        Column("responsavel_id", ForeignKey("usuario.id_usuario"), nullable=True),
        Column("descricao", String, nullable=True),
        Column("data_hora", DateTime, nullable=False),
        Column("data_entrega", DateTime, nullable=True),
        Column("status", String, nullable=False),
        Column("demanda_id", ForeignKey("demanda.id_demanda"), nullable=False),
    )


def init_tabela_fato(metadata):
    return Table(
        "fato",
        metadata,
        Column("id_fato", Integer, primary_key=True),
        Column("tipo", String, nullable=False),
        Column("titulo", String, nullable=False),
        Column("descricao", String),
        Column("data_hora", DateTime, nullable=False),
        Column("demanda_id", ForeignKey("demanda.id_demanda"), nullable=False),
        Column("dados", JSON),
    )


@pytest.fixture(scope="function")
def _engine():
    return create_engine("sqlite+pysqlite:///:memory:", echo=True, future=True)


@pytest.fixture(scope="function")
def _setup_db(_engine):
    metadata = MetaData()
    mapper = registry()

    mapper.map_imperatively(TipoDocumento, init_tabela_tipo_documento(metadata))
    mapper.map_imperatively(
        Documento,
        init_tabela_documento(metadata),
        properties={"tipo": relationship(TipoDocumento)},
    )
    mapper.map_imperatively(Usuario, init_tabela_usuario(metadata))
    mapper.map_imperatively(
        Tarefa,
        init_tabela_tarefa(metadata),
        properties={
            "responsavel": relationship(Usuario),
        },
    )
    mapper.map_imperatively(TipoDemanda, init_tabela_tipo_demanda(metadata))
    mapper.map_imperatively(
        Demanda,
        init_tabela_demanda(metadata),
        properties={
            "tipo": relationship(TipoDemanda, lazy="immediate"),
            "tarefas": relationship(Tarefa, backref="demanda", lazy="immediate"),
            "responsavel": relationship(Usuario, lazy="immediate"),
            "documentos": relationship(Documento, lazy="immediate"),
            "fatos": relationship(Fato, backref="demanda", lazy="immediate"),
        },
    )
    mapper.map_imperatively(Fato, init_tabela_fato(metadata))

    metadata.create_all(_engine)
    yield _engine
    mapper.dispose()
    metadata.clear()


def test_salvar_documento(_setup_db):
    eng = _setup_db
    with Session(eng) as s:
        t = TipoDocumento(nome="PROCESSO")
        s.add(d := Documento("Documento X", tipo=t))
        s.commit()

    with Session(eng) as s:
        documento: Documento = s.query(Documento).get(1)
        assert documento

    assert documento.id_documento


def test_db_usuario(_setup_db):
    engine = _setup_db
    with Session(engine) as s:
        s.add(Usuario("Leonardo", "123456"))
        s.commit()

    with Session(engine) as s:
        u = s.query(Usuario).get(1)

    assert u


def test_db_tipo_demanda(_setup_db):
    engine = _setup_db
    with Session(engine) as s:
        s.add(TipoDemanda(nome="PROCESSO"))
        s.commit()

    with Session(engine) as s:
        tp = s.query(TipoDemanda).get(1)

    assert tp


def test_db_demanda(_setup_db):
    engine = _setup_db
    with Session(engine) as s:
        tp_doc = TipoDocumento(nome="PROCESSO")

        s.add(
            Demanda(
                TipoDemanda(nome="Alteração"),
                "Alteração de Domingo",
                documentos=[Documento("1", tipo=tp_doc), Documento("2", tipo=tp_doc)],
                responsavel=Usuario("Leonardo", "12345678"),
                tarefas=[Tarefa("1")],
            )
        )
        s.commit()

    with Session(engine) as s:
        demanda: Demanda = s.query(Demanda).get(1)

    assert demanda
    assert demanda.tarefas
    assert demanda.documentos
    assert demanda.responsavel


def test_db_tarefa(_setup_db):
    engine = _setup_db
    with Session(engine) as s:
        s.add(Tarefa("Criar Mapa", demanda=Demanda(TipoDemanda("-"), "PROCESSO")))
        s.commit()

    with Session(engine):
        t: Tarefa = s.query(Tarefa).get(1)

    assert t
    assert t.demanda


def test_db_fato(_setup_db):
    engine = _setup_db
    with Session(engine) as s:
        s.add(
            Fato(
                "E-mail enviado",
                TipoFatos.SIMPLES,
                demanda=Demanda(TipoDemanda("-"), "X"),
                dados={},
            )
        )
        s.commit()

    with Session(engine) as s:
        f = s.query(Fato).get(1)

    assert f

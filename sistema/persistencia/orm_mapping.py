from sqlalchemy import (
    JSON,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    MetaData,
    String,
    Table,
)
from sqlalchemy.orm import relationship
from sqlalchemy.engine import Engine

from sistema.model.entidades.demanda import Demanda, TipoDemanda
from sistema.model.entidades.documento import Documento, TipoDocumento
from sistema.model.entidades.fato import Fato
from sistema.model.entidades.tarefa import Tarefa
from sistema.model.entidades.usuario import Usuario


def mapear(engine: Engine, metadata: MetaData, mapper) -> MetaData:
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

    metadata.create_all(engine)
    return metadata


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
        Column("nome", String, nullable=False),
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
        Column("nome", String, nullable=False, unique=True),
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
        Column("status", String, nullable=False),
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

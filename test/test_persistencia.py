from sqlalchemy import (
    MetaData,
    event,
    create_engine,
)
from sqlalchemy.orm import registry, relationship, Session
from sqlalchemy.engine import Engine
import pytest
from sistema.model.entidades.demanda import Demanda, TipoDemanda

from sistema.model.entidades.documento import TipoDocumento, Documento
from sistema.model.entidades.fato import Fato, TipoFatos
from sistema.model.entidades.tarefa import Tarefa
from sistema.model.entidades.usuario import Usuario
from sistema.persistencia.orm_mapping import mapear
from sistema.persistencia.realizar_operacao_com_db import realizar_operacao_com_db
from sistema.persistencia.operacoes import obter_todos_tipos_demanda
from test.fixtures import temp_db, faker_obj


@pytest.fixture(scope="function")
def _engine():
    return create_engine("sqlite+pysqlite:///:memory:", echo=True, future=True)


@pytest.fixture(scope="function")
def _setup_db(_engine):
    metadata = MetaData()
    mapper = registry()

    mapear(_engine, metadata, mapper)

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
                tipo=TipoDemanda(nome="Alteração"),
                titulo="Alteração de Domingo",
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
        s.add(
            Tarefa(
                titulo="Criar Mapa",
                demanda=Demanda(tipo=TipoDemanda(nome="-"), titulo="PROCESSO"),
            )
        )
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
                titulo="E-mail enviado",
                tipo=TipoFatos.SIMPLES,
                demanda=Demanda(tipo=TipoDemanda("-"), titulo="X"),
                dados={},
            )
        )
        s.commit()

    with Session(engine) as s:
        f = s.query(Fato).get(1)

    assert f


def test_obter_todos_tipos_demanda(temp_db, faker_obj):
    temp_db.add_all([TipoDemanda(nome=faker_obj.bothify("?????")) for _ in range(0, 5)])
    temp_db.commit()

    tp_dem = realizar_operacao_com_db(temp_db, obter_todos_tipos_demanda)
    assert len(tp_dem) == 5

from datetime import datetime
from test.fixtures import faker_obj, temp_db

import pytest
from sqlalchemy import MetaData, create_engine, event, select
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, registry, relationship

from sistema.model.entidades.demanda import Demanda, TipoDemanda
from sistema.model.entidades.documento import Documento, TipoDocumento
from sistema.model.entidades.fato import Fato, TipoFatos
from sistema.model.entidades.tarefa import Tarefa
from sistema.model.entidades.usuario import Usuario
from sistema.model.operacoes.usuario import definir_senha
from sistema.persistencia.operacoes import (
    obter_todos_tipos_demanda,
    usuario_com_este_nome_existe,
    tipo_demanda_com_este_nome_existe,
    consultar_demandas,
)
from sistema.persistencia.orm_mapping import mapear, criar_tabelas
from sistema.persistencia.realizar_operacao_com_db import realizar_operacao_com_db
from sistema.persistencia.operacoes import consultar_demandas
from sistema.persistencia import setup_persistencia


@pytest.fixture(scope="function")
def _engine():
    return create_engine("sqlite+pysqlite:///:memory:", echo=True, future=True)


@pytest.fixture(scope="function")
def _setup_db(_engine):
    metadata = MetaData()
    mapper = registry()

    mapear(metadata, mapper)
    criar_tabelas(_engine, metadata)

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


def test_nome_usuario_existe(temp_db):
    existe = realizar_operacao_com_db(
        temp_db, lambda db: usuario_com_este_nome_existe(db, "Leo")
    )
    assert not existe


def test_nome_usuario_existe_true(temp_db):
    nome = "João"

    temp_db.add(definir_senha(Usuario(nome), "123456"))
    temp_db.commit()

    existe = realizar_operacao_com_db(
        temp_db, lambda db: usuario_com_este_nome_existe(db, nome)
    )
    assert existe


def test_tipo_demanda_existe(temp_db):
    nome = "Processo"

    temp_db.add(TipoDemanda(nome))
    temp_db.commit()

    existe = realizar_operacao_com_db(
        temp_db, lambda db: tipo_demanda_com_este_nome_existe(db, nome)
    )

    assert existe


def test_consultar_demandas(temp_db):
    temp_db.add(Demanda("Demanda 1", TipoDemanda("1"), status="PENDENTE"))
    temp_db.commit()

    resultado = consultar_demandas(
        temp_db, {"status": "PENDENTE", "titulo": "Demanda 1"}
    )

    assert resultado


def test_setup_persistencia():
    setup_persistencia("sqlite+pysqlite:///:memory:")


def test_setup_persistencia_db_estabelecido(tmp_path):
    caminho = tmp_path / "db_teste.sqlite"
    url = f"sqlite+pysqlite:///{caminho}"
    db, reg, meta = setup_persistencia(url)
    reg.dispose()
    db.remove()
    setup_persistencia(url)


def test_consulta_demanda_por_data(temp_db):
    temp_db.add(
        Demanda("1", TipoDemanda("1"), data_entrega=datetime(2022, 2, 1, 15, 0))
    )
    temp_db.commit()

    resultado = consultar_demandas(
        temp_db,
        {
            "periodo_data_criacao_fim": None,
            "periodo_data_criacao_inicio": None,
            "periodo_data_entrega_inicio": None,
            "responsavel_id": None,
            "status": None,
            "tipo_id": None,
            "titulo": None,
            "periodo_data_entrega_inicio": datetime(2022, 1, 1),
            "periodo_data_entrega_fim": datetime(2023, 1, 1),
        },
    )
    assert len(resultado) == 1

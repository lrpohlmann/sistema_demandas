from datetime import datetime
from typing import Dict, List, Literal, Optional, Sequence, TypedDict
from sqlalchemy import select
from sqlalchemy.orm import Session

from sistema.model.entidades import TipoDemanda, Usuario, TipoDocumento
from sistema.model.entidades.demanda import Demanda
from sistema.persistencia.operadores import ArgsOperacaoPersistencia, realizar_operacao


def obter_todos_tipos_demanda(db: Session) -> List[TipoDemanda]:
    return db.execute(select(TipoDemanda)).scalars().all()


def usuario_com_este_nome_existe(db: Session, nome: str) -> bool:
    consulta = db.execute(select(Usuario).where(Usuario.nome == nome)).scalars().all()
    if not consulta:
        return False

    return True


def tipo_demanda_com_este_nome_existe(db, nome) -> bool:
    existe = (
        db.execute(select(TipoDemanda).where(TipoDemanda.nome == nome)).scalars().all()
    )
    if not existe:
        return False

    return True


def tipo_documento_com_este_nome_existe(db, nome: str) -> bool:
    existe = (
        db.execute(select(TipoDocumento).where(TipoDocumento.nome == nome))
        .scalars()
        .all()
    )
    if not existe:
        return False

    return True


class DadosConsultaDemandaDict(TypedDict):
    titulo: Optional[str]
    responsavel_id: Optional[int]
    tipo_id: Optional[int]
    periodo_data_criacao_inicio: Optional[datetime]
    periodo_data_criacao_fim: Optional[datetime]
    periodo_data_entrega_inicio: Optional[datetime]
    periodo_data_entrega_fim: Optional[datetime]
    status: Optional[Literal["PENDENTE", "RESOLVIDO", ""]]


def consultar_demandas(
    db, dados_consulta: DadosConsultaDemandaDict
) -> Sequence[Demanda]:
    templates_consulta_por_campo = [
        ArgsOperacaoPersistencia(Demanda.titulo, "EQ", dados_consulta.get("titulo")),
        ArgsOperacaoPersistencia(
            Demanda.responsavel_id, "EQ", dados_consulta.get("responsavel_id")
        ),
        ArgsOperacaoPersistencia(Demanda.tipo_id, "EQ", dados_consulta.get("tipo_id")),
        ArgsOperacaoPersistencia(
            Demanda.data_criacao,
            "GE",
            dados_consulta.get("periodo_data_criacao_inicio"),
        ),
        ArgsOperacaoPersistencia(
            Demanda.data_criacao, "LT", dados_consulta.get("periodo_data_criacao_fim")
        ),
        ArgsOperacaoPersistencia(
            Demanda.data_entrega,
            "GE",
            dados_consulta.get("periodo_data_entrega_inicio"),
        ),
        ArgsOperacaoPersistencia(
            Demanda.data_entrega, "LE", dados_consulta.get("periodo_data_entrega_fim")
        ),
        ArgsOperacaoPersistencia(Demanda.status, "EQ", dados_consulta.get("status")),
    ]

    consuta = select(Demanda).where(
        *[
            realizar_operacao(template.alvo, template.operacao, template.dado)
            for template in templates_consulta_por_campo
            if template.dado is not None
        ]
    )

    return db.execute(consuta).scalars().all()

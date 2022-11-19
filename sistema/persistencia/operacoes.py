from datetime import datetime
from typing import Dict, List, Literal, Optional, Sequence, TypedDict
from sqlalchemy import select
from sqlalchemy.orm import Session

from sistema.model.entidades import TipoDemanda, Usuario, TipoDocumento
from sistema.model.entidades.demanda import Demanda
from sistema.persistencia import operadores


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
    operacao_por_dado: Dict[str, operadores._literal_operacoes] = {
        "titulo": operadores.EQ,
        "responsavel_id": operadores.EQ,
        "tipo_id": operadores.EQ,
        "periodo_data_criacao_inicio": operadores.GE,
        "periodo_data_criacao_fim": operadores.LE,
        "periodo_data_entrega_inicio": operadores.GE,
        "periodo_data_entrega_fim": operadores.LE,
        "status": operadores.EQ,
    }

    campos_por_dado = {
        "titulo": Demanda.titulo,
        "responsavel_id": Demanda.responsavel_id,
        "tipo_id": Demanda.tipo_id,
        "periodo_data_criacao_inicio": Demanda.data_criacao,
        "periodo_data_criacao_fim": Demanda.data_criacao,
        "periodo_data_entrega_inicio": Demanda.data_entrega,
        "periodo_data_entrega_fim": Demanda.data_entrega,
        "status": Demanda.status,
    }

    dados_filtrados = dict(
        [(nome, dado) for nome, dado in dados_consulta.items() if dado is not None]
    )

    consuta = select(Demanda).where(
        *[
            operadores.realizar_operacao(
                campos_por_dado[campo], operacao_por_dado[campo], dado
            )
            for campo, dado in dados_filtrados.items()
        ]
    )

    return db.execute(consuta).scalars().all()

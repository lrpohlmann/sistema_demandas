from typing import List
from sqlalchemy import select
from sqlalchemy.orm import Session

from sistema.model.entidades import TipoDemanda, Usuario


def obter_todos_tipos_demanda(db: Session) -> List[TipoDemanda]:
    return db.execute(select(TipoDemanda)).scalars().all()


def usuario_com_este_nome_existe(db: Session, nome: str) -> bool:
    consulta = db.execute(select(Usuario).where(Usuario.nome == nome)).scalars().all()
    if not consulta:
        return False

    return True

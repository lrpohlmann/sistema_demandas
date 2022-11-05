from typing import List
from sqlalchemy import select
from sqlalchemy.orm import Session

from sistema.model.entidades import TipoDemanda


def obter_todos_tipos_demanda(db: Session) -> List[TipoDemanda]:
    return db.execute(select(TipoDemanda)).scalars().all()

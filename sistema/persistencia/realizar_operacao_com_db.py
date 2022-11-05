from sqlalchemy.orm import Session

from typing import TypeVar, Callable

T = TypeVar("T")


def realizar_operacao_com_db(db: Session, operacao: Callable[[Session], T]) -> T:
    with db.begin():
        return operacao(db)

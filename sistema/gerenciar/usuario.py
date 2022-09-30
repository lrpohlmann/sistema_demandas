from sqlalchemy.orm import scoped_session

from sistema.persistencia import setup_persistencia
from sistema.model.entidades.usuario import Usuario
from sistema.model.operacoes.usuario import definir_senha


def criar_usuario(db: scoped_session, nome: str, senha: str):
    db.add(definir_senha(Usuario(nome), senha))
    db.commit()

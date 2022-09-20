from typing import Protocol
import bcrypt


class _TemSenha(Protocol):
    senha: str


def definir_senha(usuario: _TemSenha, senha_fornecida: str) -> _TemSenha:
    usuario.senha = bcrypt.hashpw(
        password=senha_fornecida.encode("utf-8"), salt=bcrypt.gensalt()
    ).decode("utf-8")

    return usuario


def confirmar_senha(usuario: _TemSenha, senha_fornecida: str) -> bool:
    return bcrypt.checkpw(
        senha_fornecida.encode("utf-8"), usuario.senha.encode("utf-8")
    )

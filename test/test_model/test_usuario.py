from sistema.model.operacoes import usuario
from sistema.model.entidades.usuario import Usuario


def test_definir_senha():
    u = Usuario(nome="u1")
    usuario_senha_definida = usuario.definir_senha(u, "amcjdkncaksl")
    assert usuario_senha_definida.senha


def test_confirmar_senha():
    u = Usuario(nome="u1")
    senha = "saicslafrpso"
    usuario_com_senha = usuario.definir_senha(u, senha)

    assert usuario.confirmar_senha(usuario_com_senha, senha)

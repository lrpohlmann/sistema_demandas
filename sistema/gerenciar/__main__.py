import argparse
from ast import parse

from sistema.persistencia import setup_persistencia
from sistema.gerenciar.db import despopular_db, popular_db
from sistema.gerenciar.usuario import criar_usuario

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Aplicações para gerenciar Sistema Demanda"
    )
    grupo = parser.add_mutually_exclusive_group()
    grupo.add_argument("--db", choices=["popular", "despopular"])

    grupo.add_argument("--u", action="store_true")

    argumentos = vars(parser.parse_args())

    if argumentos["db"]:
        db, reg, meta = setup_persistencia("sqlite+pysqlite:///db.sqlite")

        if argumentos["db"] == "popular":
            popular_db(db)
            print("Populado.")
        elif argumentos["db"] == "despopular":
            despopular_db(meta)
            print("Despopulado.")

    elif argumentos["u"]:
        db, reg, meta = setup_persistencia("sqlite+pysqlite:///db.sqlite")

        print("Criar Usuário: \n")
        nome = input("Nome do usuário: ")
        senha = input("Senha: ")

        try:
            criar_usuario(db, nome, senha)
        except Exception as e:
            print("Falha ao criar usuário")
            print(e)

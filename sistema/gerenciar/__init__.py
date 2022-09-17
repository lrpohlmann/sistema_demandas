import argparse
from ast import parse

from sistema.persistencia import setup_persistencia
from sistema.gerenciar.db import despopular_db, popular_db

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Aplicações para gerenciar Sistema Demanda"
    )
    grupo = parser.add_mutually_exclusive_group()
    grupo.add_argument("--db", choices=["popular", "despopular"])

    argumentos = vars(parser.parse_args())

    if argumentos["db"]:
        db, reg, meta = setup_persistencia("sqlite+pysqlite:///db.sqlite")

        if argumentos["db"] == "popular":
            popular_db(db)
            print("Populado.")
        elif argumentos["db"] == "despopular":
            despopular_db(meta)
            print("Despopulado.")

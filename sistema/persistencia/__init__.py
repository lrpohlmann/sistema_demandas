from importlib_metadata import metadata
from sqlalchemy.orm import scoped_session, sessionmaker, registry
from sqlalchemy import MetaData, create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.event import listen

from sistema.persistencia.orm_mapping import mapear, criar_tabelas


def ativar_chave_estrangeira_sqlite(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


def desativar_chave_estrangeira_sqlite(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=OFF")
    cursor.close()


def setup_persistencia(db_path: str):
    listen(Engine, "connect", ativar_chave_estrangeira_sqlite)
    engine = create_engine(db_path, future=True)
    mapper = registry()
    metadata = MetaData(bind=engine)

    mapear(metadata, mapper)
    criar_tabelas(engine, metadata)

    return (
        scoped_session(
            sessionmaker(
                bind=engine,
                autocommit=False,
                autoflush=False,
            )
        ),
        mapper,
        metadata,
    )

from importlib_metadata import metadata
from sqlalchemy.orm import scoped_session, sessionmaker, registry
from sqlalchemy import MetaData, create_engine, event
from sqlalchemy.engine import Engine

from sistema.persistencia.orm_mapping import mapear, criar_tabelas


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


def setup_persistencia(db_path: str):
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

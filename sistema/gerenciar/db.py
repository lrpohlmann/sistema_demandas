import sqlalchemy
from sqlalchemy.orm import Session
import faker
import random

from sistema.model.entidades import demanda, documento, fato, tarefa, usuario

fake = faker.Faker()


def popular_db(db: Session, fake=fake):
    db.add_all(
        [demanda.TipoDemanda(fake.bothify(text="??????????")) for _ in range(0, 3)]
    )
    db.commit()

    db.add_all(
        [
            usuario.Usuario(fake.name(), str(fake.random_number(digits=6)))
            for _ in range(0, 3)
        ]
    )

    db.commit()

    colecao_tipo_demanda = (
        db.execute(sqlalchemy.select(demanda.TipoDemanda)).scalars().all()
    )

    colecao_usuarios = db.execute(sqlalchemy.select(demanda.Usuario)).scalars().all()

    db.add_all(
        [
            demanda.Demanda(
                titulo=fake.bothify("?????????????"),
                tipo=random.choice(colecao_tipo_demanda),
                responsavel=random.choice(colecao_usuarios),
                data_entrega=random.choice([fake.date_between(), None]),
                status=random.choice(["PENDENTE", "RESOLVIDO"]),
            )
            for _ in range(0, 31)
        ]
    )

    db.commit()

    db.close()


def despopular_db(meta: sqlalchemy.MetaData):
    meta.drop_all()

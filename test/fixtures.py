import pytest
import faker

from sistema.persistencia import setup_persistencia


@pytest.fixture
def temp_db():
    db, reg, meta = setup_persistencia("sqlite+pysqlite:///:memory:")
    yield db
    reg.dispose()
    db.remove()


@pytest.fixture
def faker_obj():
    return faker.Faker()

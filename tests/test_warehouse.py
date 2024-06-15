import pytest
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from schema import Base

DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/medical_data_warehouse"

@pytest.fixture(scope='module')
def db_engine():
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)

@pytest.fixture(scope='function')
def db_session(db_engine):
    connection = db_engine.connect()
    transaction = connection.begin()
    Session = sessionmaker(bind=connection)
    session = Session()
    yield session
    session.close()
    transaction.rollback()
    connection.close()

def test_database_schema(db_session):
    # Test if the tables are created correctly
    inspector = sqlalchemy.inspect(db_session.bind)
    assert inspector.has_table('your_table_name')
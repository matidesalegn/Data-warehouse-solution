from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database connection parameters
db_params = {
    'dbname': 'data_warehouse',
    'user': 'postgres',
    'password': 'Mati@1993',
    'host': 'localhost',
    'port': 5432
}

# SQLAlchemy database URL format
SQLALCHEMY_DATABASE_URL = f"postgresql://{db_params['user']}:{db_params['password']}@{db_params['host']}:{db_params['port']}/{db_params['dbname']}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# ATENÇÃO: Substitua 'postgres' pelo seu usuário e 'suasenha' pela sua senha do PostgreSQL
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:garbim@localhost/point_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Função para garantir que a conexão abra e feche corretamente a cada requisição
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

SQLALCHEMY_DATABASE_URL = "sqlite:/// ../../todosapp.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL,connect_args={"check_same_thread":False})
SessionLocal = sessionmaker(bind=engine,autoflush=False,autocommit=False)
Base = declarative_base()

#yeld e para permitir que execute a cada momento que precisa e para
#exemplo de for uma lsita de 0 a 10, cada vezz que interar nessa lista retorna 1 ,pausa depois 2
#então e uma forma perfformatica de começar a sesão do banco de dados
def get_database():
    db = SessionLocal()
    try:
        yield  db
    finally:
        db.close()
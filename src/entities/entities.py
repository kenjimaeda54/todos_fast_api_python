from sqlalchemy import Integer,String,Column,Boolean,ForeignKey

from src.infra.database import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer,primary_key=True,index=True)
    email = Column(String,unique=True)
    user_name = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean,default=True)
    role = Column(String)


class Todos(Base):
    __tablename__ = "todos"

    id = Column(Integer,primary_key=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    completed = Column(Boolean,default=False)
    #forenkey tem que ser nomedatabela.chave
    #por isso é users_id
    owner_id = Column(Integer, ForeignKey("users.id"))
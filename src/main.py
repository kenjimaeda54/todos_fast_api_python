from fastapi import FastAPI

from src.routes import users
from src.routes import  todos
from src.infra.database import  Base,engine


##como importar algo de um arquivo
##database é um arquivo é la possui engine

app = FastAPI()

app.include_router(users.router)
app.include_router(todos.router)

Base.metadata.create_all(bind=engine)










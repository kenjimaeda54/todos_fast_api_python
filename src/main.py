import uvicorn
from fastapi import FastAPI

from src.routes import auth
from src.routes import users
from src.routes import  todos
from src.routes import admin
from src.infra.database import  Base,engine


##como importar algo de um arquivo
##database é um arquivo é la possui engine

app = FastAPI()

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)

Base.metadata.create_all(bind=engine)





if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)




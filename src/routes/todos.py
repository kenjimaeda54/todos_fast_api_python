from typing import Annotated, cast

from fastapi import Depends, HTTPException, APIRouter
from fastapi.params import Path, Body
from sqlalchemy.orm import Session
from starlette import status

from ..entities.entities import Todos
from ..infra.database import get_database
from ..models.todos.todo_request import TodosRequest
from ..routes.auth import get_current_user

# tags organiza o swager
# prefix é para adicoinar no roteador
# exemplo aqui todos serão acessados apos o /baseurl/todos/nosos recursos
router = APIRouter(
    prefix="/todos",
    tags=["todos"]
)

depends_database = Annotated[Session, Depends(get_database)]
depends_user = Annotated[dict, Depends(get_current_user)]


# Annotated e para garantir validação no casso estamos validando com o Session
# ele valida , que o dado eserpado e oque esta no db.query
# seria boa pratica usar o annotaded junto com o Path e o Query para garantir validação dos campos
# pois insere metadados
# depends e injeção dependencia estamos injetando o banco de dados
@router.get("", status_code=status.HTTP_200_OK)
async def read_all_todos(usr: depends_user, db: depends_database):
    return db.query(Todos).filter(cast("ColumnElement[bool]", Todos.owner_id == usr.get("id"))).all()


@router.get("/{todo_id}", status_code=status.HTTP_200_OK)
async def read_only_todo(user: depends_user, db: depends_database, todo_id: Annotated[int, Path(gt=0)]):
    todo_database = db.query(Todos).filter(cast("ColumnElement[bool]", Todos.id == todo_id)).filter(
        cast("ColumnElement[bool]", Todos.owner_id == user.get("id"))
    ).first()

    if todo_database is not None:
        return todo_database
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_todo(user: depends_user, db: depends_database, todo_request: Annotated[TodosRequest, Body()]):
    todo_model = Todos(**todo_request.model_dump(), owner_id=user.get("id"))

    # ja que passei o commit false nas configurações preciso determinr manual
    db.add(todo_model)
    db.commit()


@router.put("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(user: depends_user,
                      db: depends_database,
                      todo_request: Annotated[TodosRequest, Body()],
                      todo_id: Annotated[int, Path(gt=0)]):

    todo_database = db.query(Todos).filter(cast("ColumnElement[bool]", Todos.id == todo_id)) \
        .filter(cast("ColumnElement[bool]", Todos.owner_id == user.get("id"))).first()

    if todo_database is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")

    todo_database.title = todo_request.title
    todo_database.description = todo_request.description
    todo_database.priority = todo_request.priority
    todo_database.completed = todo_request.completed

    db.add(todo_database)
    db.commit()


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user: depends_user, db: depends_database, todo_id: Annotated[int, Path(qt=0)]):
    todo_database = db.query(Todos).filter(cast("ColumnElement[bool]", Todos.id == todo_id)) \
        .filter(cast("ColumnElement[bool]", Todos.owner_id == user.get("id"))).first()

    if todo_database is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")

    db.query(Todos).filter(cast("ColumnElement[bool]", Todos.id == todo_id)) \
        .filter(cast("ColumnElement[bool]", Todos.owner_id == user.get("id"))).delete()
    db.commit()

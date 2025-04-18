from typing import cast

from fastapi import APIRouter, Depends, HTTPException
from fastapi.params import Path
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from typing_extensions import Annotated
from starlette import status

from src.entities.entities import Todos, Users
from src.infra.database import get_database
from src.routes.auth import get_current_user

router = APIRouter(
    prefix="/admin",
    tags=["admin"]
)

depends_database = Annotated[Session, Depends(get_database)]
depends_user = Annotated[dict, Depends(get_current_user)]

crypt_password = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.get("/todos", status_code=status.HTTP_200_OK)
async def read_todos(user: depends_user, db: depends_database):
    if user.get("role") != "admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    return db.query(Todos).all()


@router.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user: depends_user, db: depends_database, todo_id: Annotated[int, Path(qt=0)]):
    if user.get("role") != "admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    db.query(Todos).filter(cast("Column[boolean]", Todos.id == todo_id)).delete()

    db.commit()




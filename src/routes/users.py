from typing import cast, Type

from fastapi import APIRouter, Depends, HTTPException
from fastapi.params import Body, Path
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from starlette import status
from typing_extensions import Annotated

from ..entities.entities import Users
from ..infra.database import get_database
from ..models.users.UserVerifiyPasswordRequest import UserPasswordRequest
from ..routes.auth import get_current_user

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

depends_database = Annotated[Session, Depends(get_database)]
depends_user = Annotated[dict, Depends(get_current_user)]

crypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.get("", status_code=status.HTTP_200_OK)
async def read_user(user: depends_user, db: depends_database):
    return db.query(Users).filter(cast("Column[boolean]", Users.id == user.get("id"))).first()


@router.put("", status_code=status.HTTP_204_NO_CONTENT)
async def update_password(user: depends_user, db: depends_database,
                          user_password_request: Annotated[UserPasswordRequest, Body()]
                          ):
    user_database: Type[Users] = db.query(Users).filter(cast("Column[bool]", Users.id == user.get("id"))).first()

    if not crypt_context.verify(user_password_request.old_password, user_database.hashed_password):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Error update password")

    user_database.hashed_password = crypt_context.hash(user_password_request.new_password)

    db.add(user_database)
    db.commit()


@router.put("/{phone_number}",status_code=status.HTTP_204_NO_CONTENT)
async def update_phone_number(user: depends_user,db: depends_database,phone_number: Annotated[str,Path()]):
    user_database: Type[Users] = db.query(Users).filter(cast("Column[bool]", Users.id == user.get("id"))).first()

    user_database.phone_number = phone_number

    db.add(user_database)
    db.commit()
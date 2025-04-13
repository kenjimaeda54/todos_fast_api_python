import datetime
from datetime import timedelta
from http.client import HTTPException
from typing import Annotated, cast, Optional, Type
from fastapi import APIRouter,Body
from fastapi.params import Depends
from sqlalchemy.orm import Session
from starlette import status
from src.entities.entities import Users
from src.infra.database import get_database
from src.models.token.token_response import TokenResponse
from src.models.users.user_request import UserRequest
from passlib.context import  CryptContext
from fastapi.security import  OAuth2PasswordRequestForm
from jose import jwt


router = APIRouter()

SECRET_KEY = "42d190947b676b9329bd2d3fe53fed66677cbad95633d5c09bcfa571254ad5f7"
ALGORITHM = "HS256"

crypt_password = CryptContext(schemes=["bcrypt"],deprecated="auto")

def  return_user_if_authenticated(user_name: str,password: str,db: Session) ->  Optional[Type[Users]]:
    user_database = db.query(Users).where(cast("Column[boolean]",Users.user_name == user_name )).first()

    if user_database is None:
        return None
    if not crypt_password.verify(password, user_database.hashed_password,):
        return None
    return user_database

def return_token_jwt(user: Type[Users],time: timedelta) -> str:
    encode = {"sub": user.user_name, "id": user.id }
    date_expires = datetime.datetime.now() + time
    encode.update({"exp": date_expires})

    return  jwt.encode(encode,SECRET_KEY,ALGORITHM)


depends_db = Annotated[Session,Depends(get_database)]

@router.post("/users",status_code=status.HTTP_204_NO_CONTENT)
async def crate_user(db: depends_db, user_request: Annotated[UserRequest,Body()]):
     user_database = Users(
         email= user_request.email,
         user_name = user_request.user_name,
         first_name = user_request.first_name,
         last_name = user_request.last_name,
         hashed_password = crypt_password.hash(user_request.password),
         is_active = True,
         role = user_request.role
     )

     db.add(user_database)
     db.commit()

@router.post("/token")
async  def  read_token_authenticated(form_data: Annotated[OAuth2PasswordRequestForm,Depends()],db: depends_db):
       user_database = return_user_if_authenticated(form_data.username,form_data.password,db)

       if user_database is None:
           return {"message:","Not authenticated"}

       token =  return_token_jwt(user_database,timedelta(minutes=20))
       return TokenResponse(
          access_token=token,
           token_type="bearer"
       )








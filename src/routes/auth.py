import datetime
from datetime import timedelta, timezone
from typing import Annotated, cast, Optional, Type
from fastapi import APIRouter,Body,HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session
from starlette import status
from src.entities.entities import Users
from src.infra.database import get_database
from src.models.token.token_response import TokenResponse
from src.models.users.user_request import UserRequest
from passlib.context import  CryptContext
from fastapi.security import  OAuth2PasswordRequestForm,OAuth2PasswordBearer
from jose import jwt,JWTError


#prefix e para separar no swager
#vai possuir uma seção apenas de auth
router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

SECRET_KEY = "42d190947b676b9329bd2d3fe53fed66677cbad95633d5c09bcfa571254ad5f7"
ALGORITHM = "HS256"

crypt_password = CryptContext(schemes=["bcrypt"],deprecated="auto")
depends_db = Annotated[Session,Depends(get_database)]

#tokenUrl é o path onde nos enviamos o bearer token
#repara que o nome é token do url
#auth é porcaus do prefix
oauth_depends = OAuth2PasswordBearer(tokenUrl='auth/token')

def  return_user_if_authenticated(user_name: str,password: str,db: Session) ->  Optional[Type[Users]]:
    user_database = db.query(Users).where(cast("Column[boolean]",Users.user_name == user_name )).first()

    if user_database is None:
        return None
    if not crypt_password.verify(password, user_database.hashed_password,):
        return None
    return user_database

def return_token_jwt(user: Type[Users],time: timedelta) -> str:
    encode = {"sub": user.user_name, "id": user.id,"role": user.role }
    #cuidado com o datetime precisa passar o timezone.utc
    #se não ira falhar o decode
    date_expires = datetime.datetime.now(timezone.utc) + time
    encode.update({"exp": date_expires})

    return  jwt.encode(encode,SECRET_KEY,algorithm=ALGORITHM)


async def get_current_user(token: Annotated[str,Depends(oauth_depends)]):
   try:
       decode = jwt.decode(token,SECRET_KEY, algorithms=[ALGORITHM],options={"verify_signature": False})
       # sub é o id que passo no encode
       user_name = decode.get("sub")
       user_id = decode.get("id")
       user_role = decode.get("role")

       if user_name is None or user_id is None:
           raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Not unauthorized")

       return {"user_name": user_name,"id": user_id,"role": user_role}
   except JWTError:
           raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not unauthorized")

@router.post("",status_code=status.HTTP_204_NO_CONTENT)
async def crate_user(db: depends_db, user_request: Annotated[UserRequest,Body()]):
     user_database = Users(
         email= user_request.email,
         user_name = user_request.user_name,
         first_name = user_request.first_name,
         last_name = user_request.last_name,
         hashed_password = crypt_password.hash(user_request.password),
         is_active = True,
         role = user_request.role,
         phone_number = user_request.phone_number
     )
     user_with_user_email = db.query(Users).where(cast("Column[boolean]", Users.email == user_database.email)).first()
     user_with_user_name = db.query(Users).where(cast("Column[boolean]", Users.user_name == user_database.user_name)).first()

     if user_with_user_email:
         raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Have someone with this email on App")

     if user_with_user_name:
         raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Have someone with this username on App")

     db.add(user_database)
     db.commit()

@router.post("/token",response_model=TokenResponse)
async  def  read_token_authenticated(form_data: Annotated[OAuth2PasswordRequestForm,Depends()],db: depends_db):
       user_database = return_user_if_authenticated(form_data.username,form_data.password,db)

       if user_database is None:
           raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not unauthorized")

       token =  return_token_jwt(user_database,timedelta(minutes=20))
       return TokenResponse(
          access_token=token,
           token_type="bearer"
       )








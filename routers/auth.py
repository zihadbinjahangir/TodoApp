from fastapi import APIRouter, Depends, HTTPException
from models import user
from typing import Optional
from passlib.context import CryptContext
from sqlalchemy.orm import session
from database import Sessionlocal, engine
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from datetime import datetime, timedelta
from jose import jwt, JWTError
from schemas.user import UserSchema
from repositories.user_repository_impl import UserRepositoryImpl

SECRET_KEY = "HelloWorld"
ALGORITHM = "HS256"

user.Base.metadata.create_all(bind=engine)
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='token')

def get_db():
    try:
        db = Sessionlocal()
        yield db
    finally:
        db.close()

def get_bcrypt_password(password):
    return bcrypt_context.hash(password)

def verify_password(plain_password, hashed_password):
    return bcrypt_context.verify(plain_password,hashed_password)

def authenticate_user(user_name:str,password:str,db):
    user_repo = UserRepositoryImpl(db)
    user = user_repo.get_user(user_name)
    if not user:
        return False
    if not verify_password(password,user.hashed_password):
        return False
    return user

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={401:{"user":"Not authorized"}}
)

def creat_access_token(user_name: str, user_id: int, expires_delta: Optional[timedelta] = None):
    encode = {'sub': user_name, 'id':user_id}
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    encode.update({'exp':expire})

    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_bearer)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        user_name = payload.get('sub')
        user_id = payload.get('id')
        if user_name is None or user_id is None:
            raise user_not_found_exception()
        return {'username':user_name,'user_id':user_id}
    except JWTError:
        raise user_not_found_exception()


@router.post("/creat/user")
async def creat_new_user(user: UserSchema, db: session = Depends(get_db)):
    user_repo = UserRepositoryImpl(db)
    user_model = user_repo.create_user(user, get_bcrypt_password(user.hashed_password))
    if user_model is not None:
        return {
        "status":201,
        "transaction":"Successful"
        }

@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm=Depends(),
                                 db: session = Depends(get_db)):
    user = authenticate_user(form_data.username,form_data.password,db)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    expires_delta = timedelta(minutes=20)
    token  = creat_access_token(user.username, user.id, expires_delta)
    return {"token":token}

def user_not_found_exception():
    return HTTPException(status_code=404, detail="User not found")
    
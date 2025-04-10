from fastapi import APIRouter,status,Depends
from models import User
from schemas import RegisterModel,LoginModel
from database import session,engine
from fastapi.exceptions import HTTPException
from werkzeug.security import generate_password_hash,check_password_hash
from fastapi_jwt_auth import AuthJWT
from sqlalchemy import or_
from fastapi.encoders import jsonable_encoder
import datetime

session = session(bind=engine)

auth_router = APIRouter(
    prefix='/auth'
)

@auth_router.get('/')
async def welcome(Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Invalid token')
    response = {
        'Message':'Bu bizning register sahifamiz'
    }
    return response

@auth_router.post('/register',status_code=status.HTTP_201_CREATED)
async def register(user:RegisterModel):
    db_email = session.query(User).filter(User.email==user.email).first()
    if db_email is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='User with this email is already exists'
        )
    db_username = session.query(User).filter(User.username==user.username).first()
    if db_username is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail = 'User with this username is already exists'
        )
    new_user = User(
        id = user.id,
        username=user.username,
        email=user.email,
        password=generate_password_hash(user.password),
        is_staff=user.is_staff,
        is_active=user.is_active
    )
    session.add(new_user)
    session.commit()

    data = {
        'id':new_user.id,
        'username':new_user.username,
        'email':new_user.email,
        'password':new_user.password,
        'is_staff':new_user.is_staff,
        'is_active':new_user.is_active
    }

    response = {
        'status':'success',
        'message':'User successfully signed up',
        'code':'201',
        'data':data
    }

    return response

@auth_router.post('/login',status_code=status.HTTP_200_OK)
async def login(user:LoginModel,Authorize:AuthJWT=Depends()):

    access_token_lifetime = datetime.timedelta(minutes=30)
    refresh_token_lifetime = datetime.timedelta(days=15)

    db_user = session.query(User).filter(
        or_(
            User.username == user.username_or_email,
            User.email == user.username_or_email
        )
    ).first()

    if db_user and check_password_hash(db_user.password,user.password):
        access_token = Authorize.create_access_token(subject=db_user.username,expires_time=access_token_lifetime)
        refresh_token = Authorize.create_refresh_token(subject=db_user.username,expires_time=refresh_token_lifetime)

        token = {
            'access':access_token,
            'refresh':refresh_token
        }

        response = {
            'status':'success',
            'code':'200',
            'message':'User successfully logged in',
            'data':token,
        }
        return jsonable_encoder(response)
    

@auth_router.get('/login/refresh')
async def refresh_token(Authorize:AuthJWT=Depends()):
    try:
        access_token_lifetime = datetime.timedelta(minutes=30)
        Authorize.jwt_refresh_token_required()
        current_user = Authorize.get_jwt_subject()

        db_user = session.query(User).filter(User.username==current_user).first()
        if db_user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='User is not found')
        
        new_access_token = Authorize.create_access_token(subject=db_user.username,expires_time=access_token_lifetime)
        response = {
            'status':'success',
            'code':'200',
            'message':'New access token is created',
            'data' : {
                'access':new_access_token
            }
        }
        return response

    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Invalid access token')


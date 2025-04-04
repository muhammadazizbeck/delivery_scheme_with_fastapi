from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi_jwt_auth import AuthJWT
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import Session
from database import session, engine
from schemas import SignUpModel, LoginModel
from models import User

auth_router = APIRouter(prefix='/auth')

db_session = session(bind=engine)

@auth_router.get('/')
async def signup_page():
    return {'message': 'Bu bizning registratsiya sahifamiz'}

@auth_router.post('/signup', status_code=status.HTTP_201_CREATED)
async def signup(user: SignUpModel):
    db_username = db_session.query(User).filter(User.username == user.username).first()
    if db_username is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='User with this username already exists'
        )

    db_email = db_session.query(User).filter(User.email == user.email).first()
    if db_email is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='User with this email already exists'
        )

    new_user = User(
        username=user.username,
        email=user.email,
        password=generate_password_hash(user.password),
        is_staff=user.is_staff,
        is_active=user.is_active
    )

    db_session.add(new_user)
    db_session.commit()
    db_session.refresh(new_user) 

    data = {
        'id': new_user.id,
        'username': new_user.username,
        'email': new_user.email,
        'password': new_user.password,  
        'is_staff': new_user.is_staff,
        'is_active': new_user.is_active
    }

    response_model = {
        'status': 'success',
        'code': '201',
        'message': 'User successfully signed up',
        'data': data
    }

    db_session.close() 
    return jsonable_encoder(response_model)

@auth_router.post('/login', status_code=status.HTTP_200_OK)
async def login(user: LoginModel, Authorize: AuthJWT = Depends()):
    db_user = db_session.query(User).filter(User.username == user.username).first()
    if db_user and check_password_hash(db_user.password, user.password):
        access_token = Authorize.create_access_token(subject=db_user.username)
        refresh_token = Authorize.create_refresh_token(subject=db_user.username)

        token = {
            'access': access_token,
            'refresh': refresh_token
        }

        response = {
            'status': 'success',
            'code': '200',
            'message': 'User successfully logged in',
            'data': token
        }

        db_session.close()
        return response

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail='Invalid username or password'
    )


     

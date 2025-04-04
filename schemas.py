from pydantic import BaseModel,Field
from fastapi_jwt_auth import AuthJWT
from typing import Optional

class SignUpModel(BaseModel):

    username:str
    email:str
    password:str
    is_active:Optional[bool]
    is_staff:Optional[bool]

    class Config:
        from_attributes=True
        json_schema_extra = {
            'example':{
                'username':'muhammadazizbeck',
                'email':'aa2004bek@gmail.com',
                'password':'Azizbek1410',
                'is_staff':False,
                'is_active':True
            }
        }

class Settings(BaseModel):
    authjwt_secret_key: str = "f548369e36f55304943658c87b9feb3e650aca8934d4c7eb069cef9f4dfaeeb6"
    authjwt_algorithm: str = "HS256"
    authjwt_access_token_expires: int = 60

@AuthJWT.load_config
def get_config():
    return Settings()


class LoginModel(BaseModel):
    username:str
    password:str
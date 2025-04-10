from pydantic import BaseModel,BaseSettings
from typing import Optional

class RegisterModel(BaseModel):
    id:Optional[int]
    username:str
    email:str
    password:str
    is_staff:Optional[bool]
    is_active:Optional[bool]

    class Config:
        from_attributes=True
        json_schema_extra={
            'example':{
                'id':'1',
                'username':'muhammadazizbeck',
                'email':'aa2004bek@gmail.com',
                'password':'Azizbek1410',
                'is_staff':False,
                'is_active':True
            }
        }

class Settings(BaseSettings):
    authjwt_secret_key:str='b7aa4bebc0ba90229c27db804c1e21c3ee9eedba27539e7c3b7cf85346124dbd'

class LoginModel(BaseModel):
    username_or_email:str
    password:str

class OrderModel(BaseModel):
    id:Optional[int]
    quantity:int
    order_statuses:Optional[str]='PENDING'
    user_id:Optional[int]
    product_id:Optional[int]

    class Config:
        from_attributes=True
        json_schema_extra={
            'example':{
                'quantity':2
            }
        }
    
class OrderStatusModel(BaseModel):
    order_statuses:Optional[str]

    class Config:
        from_attributes=True
        json_schema_extra={
            'example':{
                'quantity':2
            }
        }

class ProductModel(BaseModel):
    id:Optional[int]
    name:str
    price:int

    class Config:
        from_attributes=True
        json_scheme_extra = {
            'example':{
                'name':'Plov',
                'price':35000
            }
        }




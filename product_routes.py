from fastapi import APIRouter,status,Depends
from fastapi_jwt_auth import AuthJWT
from fastapi.exceptions import HTTPException
from schemas import ProductModel
from database import session,engine
from fastapi.encoders import jsonable_encoder
from models import User,Product

session=session(bind=engine)

product_router = APIRouter(
    prefix='/product'
)

@product_router.post('/create',status_code=status.HTTP_201_CREATED)
async def create_product(product:ProductModel,Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Please enter valid access token')
    current_user = Authorize.get_jwt_subject()
    user = session.query(User).filter(User.username==current_user).first()

    if user.is_staff:
        new_product = Product(
            name=product.name,
            price=product.price
        )
        session.add(new_product)
        session.commit()

        data = {
            'id':new_product.id,
            'name':new_product.name,
            'price':new_product.price
        }

        response = {
            "status":"success",
            'code':"201",
            'message':"Product is successfully created",
            'data':data
        }
        return jsonable_encoder(response)
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail='Only superadmins can add product')
    
@product_router.get('/list',status_code=status.HTTP_200_OK)
async def list_product(Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Please enter valid access token')
    current_user = Authorize.get_jwt_subject()
    user = session.query(User).filter(User.username==current_user).first()

    if user.is_staff:
        products = session.query(Product).all()
        response = []
        for product in products:
            response.append({
                'id':product.id,
                'name':product.name,
                'price':product.price
                })
        final_response = {
            'status':'success',
            'code':'200',
            'message':'You have successfully took product list',
            'data':response
        }
        return jsonable_encoder(final_response)
    
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Only superadmins can take product list")
    
@product_router.get('/{id}',status_code=status.HTTP_200_OK)
async def get_product_by_id(id:int,Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Please enter valid access token')
    current_user = Authorize.get_jwt_subject()
    user = session.query(User).filter(User.username==current_user).first()
    if user.is_staff:
        product = session.query(Product).filter(Product.id==id).first()
        if product:
            data = {
                'id':product.id,
                'name':product.name,
                'price':product.price,
            }
            response = {
                'status':"success",
                'code':'201',
                'data':data
            }
            return jsonable_encoder(response)
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Product with this id is not avalilable')
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail='Only super admin can see product details')
    

@product_router.post("/{id}/update", status_code=status.HTTP_200_OK)
async def update_product_by_id(id: int,update_model: ProductModel, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Please enter valid access token')

    current_user = Authorize.get_jwt_subject() 
    user = session.query(User).filter(User.username == current_user).first()

    if not user or not user.is_staff:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Only superadmins can update product')

    product = session.query(Product).filter(Product.id == id).first()

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Product with this id is not found')

    for key, value in update_model.dict(exclude_unset=True).items():
        setattr(product, key, value)

    session.commit()

    response = {
        'status': "success",
        'code': 200,
        'message': "Product is updated successfully",
        'data': {
            'id': product.id,
            'name': product.name,
            'price': product.price
        }
    }
    return jsonable_encoder(response)

    

@product_router.delete('/{id}/delete', status_code=status.HTTP_200_OK)
async def delete_product(id: int, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Please enter valid access token')

    current_user = Authorize.get_jwt_subject()
    user = session.query(User).filter(User.username == current_user).first()

    if not user or not user.is_staff:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Only superadmins can delete product')

    product = session.query(Product).filter(Product.id == id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Product with this id is not found')

    session.delete(product)
    session.commit()

    return {
        'status': 'success',
        'code': 200,
        'message': 'Product is deleted successfully'
    }


    
        
    

            


from fastapi import APIRouter,Depends,status
from fastapi.exceptions import HTTPException
from fastapi_jwt_auth import AuthJWT
from models import User,Order,Product
from database import session,engine
from schemas import OrderModel,OrderStatusModel
from fastapi.encoders import jsonable_encoder

session = session(bind=engine)

order_router = APIRouter(
    prefix='/order'
)

@order_router.get('/')
async def order_list(Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Please Enter access_token')
    response = {
        'Message':'Bu bizning order sahifamiz'
    }
    return response

@order_router.post('/make',status_code=status.HTTP_201_CREATED)
async def make_order(order:OrderModel,Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Please enter a valid access token')
    
    current_user = Authorize.get_jwt_subject()
    user = session.query(User).filter(User.username==current_user).first()

    new_order = Order(
        quantity=order.quantity
    )
    new_order.user=user

    session.add(new_order)
    session.commit()

    order = {
        'id':new_order.id,
        'quantity':new_order.quantity,
        'order_statuses':new_order.order_statuses,
    }

    response = {
        'status':'success',
        'code':'201',
        'message':'Order is created successfully',
        'data':order
    }

    return jsonable_encoder(response)

@order_router.get('/list', status_code=status.HTTP_200_OK)
async def order_list(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Please enter a valid access token')
    
    current_user = Authorize.get_jwt_subject()
    user = session.query(User).filter(User.username == current_user).first()

    if user and user.is_staff:
        orders = session.query(Order).all()

        final_response = []

        for order in orders:
            final_response.append({
                'id': order.id,
                'user': {
                    'id': order.user_id,
                    'username': order.user.username,
                    'email': order.user.email
                },
                'quantity': order.quantity,
                'order_statuses': order.order_statuses
            })

        return jsonable_encoder({
            'status': 'success',
            'code': 200,
            'message': 'All orders retrieved successfully',
            'data': final_response
        })

    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Only superadmins can see all orders')

@order_router.get('/{id}')
async def get_order_by_id(id:int,Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,datail='Please enter valid access token')
    
    current_user = Authorize.get_jwt_subject()
    user = session.query(User).filter(User.username==current_user).first()

    if user.is_staff and user.is_staff:
        order = session.query(Order).filter(Order.id==id).first()
        if order:
            order_data = {

                'id': order.id,
                'user': {
                    'id': order.user_id,
                    'username': order.user.username,
                    'email': order.user.email
                },
                'quantity': order.quantity,
                'order_statuses': order.order_statuses
            }

            final_response = {
                'status':'success',
                'code':'200',
                'message':'You have successfully took order details',
                'data':order_data
            }
            return jsonable_encoder(final_response)
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Order with this id is not avalilable")
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,datail='Only superadmin can see order details')

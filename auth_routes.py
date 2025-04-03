from fastapi import APIRouter

auth_router = APIRouter(
    prefix='/auth'
)

@auth_router.get('/')
async def register():
    return {'message':'Bu bizning registratsiya sahifamiz'}
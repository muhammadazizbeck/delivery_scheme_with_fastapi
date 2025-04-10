from database import engine,Base
from models import Order,User,Product

Base.metadata.create_all(bind=engine)
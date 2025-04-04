from database import Base,engine
from models import Product,Order,User

Base.metadata.create_all(bind=engine)

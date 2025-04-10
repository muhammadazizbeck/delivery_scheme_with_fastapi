from database import Base
from sqlalchemy import Column,Integer,String,Text,Boolean,ForeignKey
from sqlalchemy_utils.types import ChoiceType
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__='user'
    id = Column(Integer,primary_key=True)
    username = Column(String(25),unique=True)
    email = Column(String(50),unique=50)
    password = Column(Text,nullable=False)
    is_staff = Column(Boolean,default=False)
    is_active = Column(Boolean,default=False)
    orders = relationship('Order',back_populates='user')

    def __repr__(self):
        return f"<User:{self.username}"

class Order(Base):
    ORDER_STATUSES = (
        ('PENDING','pending'),
        ('IN_TRANSIT','in_transit'),
        ('DELIVERED','delivered')
    )
    __tablename__='orders'
    id = Column(Integer,primary_key=True)
    quantity = Column(Integer,nullable=False)
    order_statuses = Column(ChoiceType(choices=ORDER_STATUSES),default='PENDING')
    user_id = Column(Integer,ForeignKey('user.id'))
    user = relationship('User',back_populates='orders')
    product_id = Column(Integer,ForeignKey('product.id'))
    product = relationship('Product',back_populates='orders')

    def __repr__(self):
        return f"<Order:{self.id}"


class Product(Base):
    __tablename__='product'
    id = Column(Integer,primary_key=True)
    name = Column(String(70))
    price = Column(Integer)
    orders = relationship('Order',back_populates='product')

    def __repr__(self):
        return f"<Product:{self.name}"

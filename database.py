from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base

DATABASE_URL = 'postgresql://postgres:Azizbek1410@localhost/delivery_db'


engine = create_engine(DATABASE_URL,echo=True)


Base = declarative_base()
session = sessionmaker()
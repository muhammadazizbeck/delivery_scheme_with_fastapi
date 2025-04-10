from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base,sessionmaker


DATABASE_URL = 'postgresql://postgres:Azizbek1410@localhost/express_delivery_db'

engine = create_engine(DATABASE_URL,echo=True)
session = sessionmaker()
Base = declarative_base()
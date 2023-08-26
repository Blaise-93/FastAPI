from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
load_dotenv()


SQL_DB_URL = os.getenv("SQLALCHEMY_DB_URL")
#print(SQL_DB_URL)

engine = create_engine(SQL_DB_URL)

sessionLocal = sessionmaker(
    expire_on_commit=True,
    autoflush=False,
    bind=engine)

Base = declarative_base()


def get_db():
    db = sessionLocal()
    try:
        
        yield db
    
    finally:
        db.close()

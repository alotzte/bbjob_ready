from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import models

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:123@localhost:5432/employees"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

models.Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

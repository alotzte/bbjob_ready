from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import models

SQLALCHEMY_DATABASE_URL = "postgresql://root:BB123123!@45.9.25.238:5432/postgres"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

models.Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


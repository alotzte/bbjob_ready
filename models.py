from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(100))
    password = Column(String(100))
    surname = Column(String(100))
    name = Column(String(100))
    middlename = Column(String(100))
    email = Column(String(100))
    department_id = Column(Integer, ForeignKey('departments.id'))
    telegram_id = Column(Integer)

class Department(Base):
    __tablename__ = 'departments'
    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    users = relationship('User')
    employees = relationship('Employee')

class Employee(Base):
    __tablename__ = 'employees'
    id = Column(Integer, primary_key=True)
    department_id = Column(Integer, ForeignKey('departments.id'))
    surname = Column(String(100))
    name = Column(String(100))
    middlename = Column(String(100))
    email = Column(String(100))

class Feature(Base):
    __tablename__ = 'features'
    id = Column(Integer, primary_key=True)
    employer_id = Column(Integer, ForeignKey('employees.id'))
    salary = Column(Float)
    email_statistic = Column(Integer)
    education = Column(Integer)
    work_years = Column(Integer)

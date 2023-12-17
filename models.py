from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date, Float
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
    telegram_id = Column(Integer, nullable=True)

class Department(Base):
    __tablename__ = 'departments'
    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    users = relationship('User', backref='department_ref')
    employees = relationship('Employee', backref='department_ref')

class Employee(Base):
    __tablename__ = 'employees'
    id = Column(Integer, primary_key=True)
    department_id = Column(Integer, ForeignKey('departments.id'))
    surname = Column(String(100))
    name = Column(String(100))
    middlename = Column(String(100))
    email = Column(String(100))
    features = relationship('Feature', backref='employee_ref')

class Feature(Base):
    __tablename__ = 'features'
    id = Column(Integer, primary_key=True)
    employer_id = Column(Integer, ForeignKey('employees.id'))
    Age = Column(Float)
    BusinessTravel = Column(String)
    DistanceFromHome = Column(Float)
    Education = Column(String)
    MaritalStatus = Column(String)
    MonthlyIncome = Column(Float)
    MonthlyRate = Column(Float)
    NumCompaniesWorked = Column(Float)
    OverTime = Column(String)
    PercentSalaryHike = Column(Float)
    TotalWorkingYears = Column(Float)
    TrainingTimesLastYear = Column(Float)
    YearsAtCompany = Column(Float)
    YearsWithCurrManager = Column(Float)
    SentMessages = Column(Float)
    ReceivedMessages = Column(Float)
    AddressCount = Column(Float)
    BccCount = Column(Float)
    CcCount = Column(Float)
    HoursToRead = Column(Float)
    DaysBetweenReceiveRead = Column(Float)
    RepliedMessages = Column(Float)
    OutgoingMessageLength = Column(Float)
    MessagesOutsideWork = Column(Float)
    SentReceivedRatio = Column(Float)
    DataVolumeRatio = Column(Float)
    UnansweredQuestions = Column(Float)
    probability = Column(Float)


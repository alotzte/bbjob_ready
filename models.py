from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, ForeignKey
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


class Employee(Base):
    __tablename__ = 'employees'
    id = Column(Integer, primary_key=True)
    department_id = Column(Integer, ForeignKey('departments.id'))
    surname = Column(String(100))
    name = Column(String(100))
    middlename = Column(String(100))
    email = Column(String(100))
    features = relationship("Feature", backref="employee")


class Feature(Base):
    __tablename__ = 'features'
    id = Column(Integer, primary_key=True)
    employer_id = Column(Integer, ForeignKey('employees.id'))
    age = Column(Integer)
    education = Column(Integer, ForeignKey('education.id'))
    marital_status = Column(String)
    monthly_income = Column(Float)
    num_companies_worked = Column(Integer)
    over_time = Column(Integer)
    total_working_years = Column(Integer)
    years_at_company = Column(Integer)
    resume_on_job_search_site = Column(Integer)
    company_years_ratio = Column(Float)
    sent_messages = Column(Float)
    received_messages = Column(Float)
    message_recipients = Column(Float)
    bcc_message_count = Column(Float)
    cc_message_count = Column(Float)
    late_read_messages = Column(Float)
    days_between_received_read = Column(Float)
    replied_messages = Column(Float)
    sent_message_characters = Column(Float)
    off_hours_sent_messages = Column(Float)
    received_sent_ratio = Column(Float)
    received_sent_bytes_ratio = Column(Float)
    unanswered_questions = Column(Float)
    probability = Column(Float)


class Education(Base):
    __tablename__ = 'education'
    id = Column(Integer, primary_key=True)
    education_name = Column(String(100))

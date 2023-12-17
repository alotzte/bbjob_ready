from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import models
from models import Department, Education


SQLALCHEMY_DATABASE_URL = "postgresql://postgres:123@localhost:5432/employees"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

models.Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()



def create_initial_entries():
    # Создаем сессию
    db = SessionLocal()

    try:
        # Создаем объект отдела
        department_names = ["IT", "Human Resources", "Finance", "Marketing", "Research and Development"]

        # Создаем и добавляем отделы
        for name in department_names:
            department = Department(title=name)
            db.add(department)

        education_types = [
            "Общее образование",
            "Среднее образование",
            "Среднее специальное образование",
            "Высшее образование",
            "Два и более высших образования"
        ]

        # Создаем и добавляем виды образования
        for education_name in education_types:
            education = Education(education_name=education_name)
            db.add(education)

        # Подтверждаем изменения в базе данных
        db.commit()


    except Exception as e:
        print(f"Произошла ошибка: {e}")
        db.rollback()
    finally:
        db.close()


# Вызываем функцию для создания записей
create_initial_entries()

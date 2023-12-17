import sys
import csv

sys.path.append("..")
import csv

import pandas as pd

from fastapi import Depends, APIRouter, Request, UploadFile, File
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

from .auth import get_current_user

from starlette.responses import RedirectResponse
from starlette import status

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import csv
from io import StringIO
from starlette.responses import StreamingResponse

from ml_model import prediction

router = APIRouter(
    prefix="/employees",
    tags=["employees"],
    responses={404: {"description": "Not found"}}
)

models.Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="templates")


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@router.get("/", response_class=HTMLResponse)
async def read_all_by_user(request: Request, db: Session = Depends(get_db)):
    user_data = await get_current_user(request)
    if user_data is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)

    user = db.query(models.User).filter(models.User.id == user_data["id"]).first()
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)

    employees = db.query(models.Employee).filter(models.Employee.department_id == user.department_id).all()

    return templates.TemplateResponse("home.html", {"request": request, "employees": employees, "user": user})


@router.post("/add-csv")
async def add_csv(request: Request, db: Session = Depends(get_db), file: UploadFile = File(...)):
    user_data = await get_current_user(request)
    if user_data is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)

    contents = await file.read()
    reader = csv.reader(contents.decode('utf-8').splitlines())

    # Пропускаем заголовок файла, если он есть
    next(reader, None)

    features_data = []

    for row in reader:
        # Создаем объект Employee
        new_employee = models.Employee(
            department_id=row[0],  # Индекс столбца в CSV для department_id
            surname=row[1],  # Индекс столбца в CSV для surname
            name=row[2],  # Индекс столбца в CSV для name
            middlename=row[3],  # Индекс столбца в CSV для middlename
            email=row[4]  # Индекс столбца в CSV для email
        )
        db.add(new_employee)
        db.flush()  # Получаем ID добавленного сотрудника

        features_row = [
            float(row[5]),  # Пример индекса для Age
            str(row[6]),  # Пример индекса для BusinessTravel
            float(row[7]),  # Пример индекса для DistanceFromHome
            float(row[8]),  # Пример индекса для Education
            str(row[9]),  # Пример индекса для MaritalStatus
            float(row[10]),  # Пример индекса для MonthlyIncome
            float(row[11]),  # Пример индекса для MonthlyRate
            float(row[12]),  # Пример индекса для NumCompaniesWorked
            str(row[13]),  # Пример индекса для OverTime
            float(row[14]),  # Пример индекса для PercentSalaryHike
            float(row[15]),  # Пример индекса для TotalWorkingYears
            float(row[16]),  # Пример индекса для TrainingTimesLastYear
            float(row[17]),  # Пример индекса для YearsAtCompany
            float(row[18]),  # Пример индекса для YearsWithCurrManager
            float(row[19]),  # Пример индекса для SentMessages
            float(row[20]),  # Пример индекса для ReceivedMessages
            float(row[21]),  # Пример индекса для AddressCount
            float(row[22]),  # Пример индекса для BccCount
            float(row[23]),  # Пример индекса для CcCount
            float(row[24]),  # Пример индекса для HoursToRead
            float(row[25]),  # Пример индекса для DaysBetweenReceiveRead
            float(row[26]),  # Пример индекса для RepliedMessages
            float(row[27]),  # Пример индекса для OutgoingMessageLength
            float(row[28]),  # Пример индекса для MessagesOutsideWork
            float(row[29]),  # Пример индекса для SentReceivedRatio
            float(row[30]),  # Пример индекса для DataVolumeRatio
            float(row[31]),  # Пример индекса для UnansweredQuestions
        ]
        features_data.append(features_row)

        features_df = pd.DataFrame(features_data, columns=['age', 'Education', 'MaritalStatus', 'MonthlyIncome',
       'NumCompaniesWorked', 'OverTime', 'TotalWorkingYears', 'YearsAtCompany',
       'ResumeOnJobSearchSite', 'CompanyYearsRatio', 'SentMessages',
       'ReceivedMessages', 'MessageRecipients', 'BccMessageCount',
       'CcMessageCount', 'LateReadMessages', 'DaysBetweenReceivedRead',
       'RepliedMessages', 'SentMessageCharacters', 'OffHoursSentMessages',
       'ReceivedSentRatio', 'ReceivedSentBytesRatio', 'UnansweredQuestions'])

        features_data.clear()
        print(features_df)


        # Создаем объект Feature, связанный с этим сотрудником
        new_feature = models.Feature(
            employer_id=new_employee.id,
            Age=row[5],  # Пример индекса для Age
            BusinessTravel=row[6],  # Пример индекса для BusinessTravel
            DistanceFromHome=row[7],  # Пример индекса для DistanceFromHome
            Education=row[8],  # Пример индекса для Education
            MaritalStatus=row[9],  # Пример индекса для MaritalStatus
            MonthlyIncome=row[10],  # Пример индекса для MonthlyIncome
            MonthlyRate=row[11],  # Пример индекса для MonthlyRate
            NumCompaniesWorked=row[12],  # Пример индекса для NumCompaniesWorked
            OverTime=row[13],  # Пример индекса для OverTime
            PercentSalaryHike=row[14],  # Пример индекса для PercentSalaryHike
            TotalWorkingYears=row[15],  # Пример индекса для TotalWorkingYears
            TrainingTimesLastYear=row[16],  # Пример индекса для TrainingTimesLastYear
            YearsAtCompany=row[17],  # Пример индекса для YearsAtCompany
            YearsWithCurrManager=row[18],  # Пример индекса для YearsWithCurrManager
            SentMessages=row[19],  # Пример индекса для SentMessages
            ReceivedMessages=row[20],  # Пример индекса для ReceivedMessages
            AddressCount=row[21],  # Пример индекса для AddressCount
            BccCount=row[22],  # Пример индекса для BccCount
            CcCount=row[23],  # Пример индекса для CcCount
            HoursToRead=row[24],  # Пример индекса для HoursToRead
            DaysBetweenReceiveRead=row[25],  # Пример индекса для DaysBetweenReceiveRead
            RepliedMessages=row[26],  # Пример индекса для RepliedMessages
            OutgoingMessageLength=row[27],  # Пример индекса для OutgoingMessageLength
            MessagesOutsideWork=row[28],  # Пример индекса для MessagesOutsideWork
            SentReceivedRatio=row[29],  # Пример индекса для SentReceivedRatio
            DataVolumeRatio=row[30],  # Пример индекса для DataVolumeRatio
            UnansweredQuestions=row[31],  # Пример индекса для UnansweredQuestions
            probability=prediction(features_df)  # Пример индекса для probability
        )
        db.add(new_feature)

    db.commit()

    return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)


@router.get("/export-csv")
async def export_csv(db: Session = Depends(get_db)):
    # Получаем данные из базы данных
    result = db.execute(select(models.Employee))
    employees = result.scalars().all()

    # Подготовка CSV файла
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['department_id', 'surname', 'name', 'middlename', 'email'])  # Заголовки столбцов

    # Запись данных сотрудников в CSV
    for employee in employees:
        writer.writerow([employee.department_id, employee.surname, employee.name, employee.middlename, employee.email])

    output.seek(0)

    headers = {
        'Content-Disposition': 'attachment; filename="employees.csv"'
    }
    return StreamingResponse(iter([output.getvalue()]), media_type="text/csv", headers=headers)

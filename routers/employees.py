import sys
import csv

sys.path.append("..")
import csv

import pandas as pd
from sqlalchemy.orm import joinedload

from fastapi import Depends, APIRouter, Request, UploadFile, File
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session, joinedload

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

    # Получение сотрудников и их свойств
    employees_with_features = db.query(models.Employee).options(joinedload(models.Employee.features))\
                                .filter(models.Employee.department_id == user.department_id).all()

    # Выбор и округление последней вероятности увольнения для каждого сотрудника
    for employee in employees_with_features:
        last_feature = max(employee.features, key=lambda x: x.id) if employee.features else None
        employee.latest_probability = int(round(last_feature.probability, 2)*100) if last_feature else None
    # Сортировка сотрудников по вероятности увольнения от большего к меньшему
    sorted_employees = sorted(employees_with_features, key=lambda x: x.latest_probability or 0, reverse=True)
    return templates.TemplateResponse("home.html", {"request": request, "employees": sorted_employees, "user": user})


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
        existing_employee = db.query(models.Employee).filter_by(email=row[4]).first()

        if existing_employee is None:
            new_employee = models.Employee(
                department_id=row[0],  # Индекс для department_id
                surname=row[1],  # Индекс для surname
                name=row[2],  # Индекс для name
                middlename=row[3],  # Индекс для middlename
                email=row[4]  # Индекс для email
            )
            db.add(new_employee)
            db.flush()
            employee_id = new_employee.id  # ID нового сотрудника
        else:
            # Если сотрудник существует, используем его ID
            employee_id = existing_employee.id

        features_row = [
            float(row[5]),  # Пример индекса для Age
            int(row[6]),  # Пример индекса для BusinessTravel
            str(row[7]),  # Пример индекса для DistanceFromHome
            float(row[8]),  # Пример индекса для Education
            int(row[9]),  # Пример индекса для MaritalStatus
            int(row[10]),  # Пример индекса для MonthlyIncome
            int(row[11]),  # Пример индекса для MonthlyRate
            int(row[12]),  # Пример индекса для NumCompaniesWorked
            int(row[13]),  # Пример индекса для OverTime
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

        ]
        features_data.append(features_row)

        features_df = pd.DataFrame(features_data, columns=['age', 'Education', 'MaritalStatus', 'MonthlyIncome',
                                                           'NumCompaniesWorked', 'OverTime', 'TotalWorkingYears',
                                                           'YearsAtCompany',
                                                           'ResumeOnJobSearchSite', 'CompanyYearsRatio', 'SentMessages',
                                                           'ReceivedMessages', 'MessageRecipients', 'BccMessageCount',
                                                           'CcMessageCount', 'LateReadMessages',
                                                           'DaysBetweenReceivedRead',
                                                           'RepliedMessages', 'SentMessageCharacters',
                                                           'OffHoursSentMessages',
                                                           'ReceivedSentRatio', 'ReceivedSentBytesRatio',
                                                           'UnansweredQuestions'])

        features_data.clear()

        # Создаем объект Feature, связанный с этим сотрудником
        new_feature = models.Feature(
            employer_id=employee_id,
            age=row[5],  # Пример индекса для Age
            education=row[6],  # Пример индекса для BusinessTravel
            marital_status=row[7],  # Пример индекса для DistanceFromHome
            monthly_income=row[8],  # Пример индекса для Education
            num_companies_worked=row[9],  # Пример индекса для MaritalStatus
            over_time=row[10],  # Пример индекса для MonthlyIncome
            total_working_years=row[11],  # Пример индекса для MonthlyRate
            years_at_company=row[12],  # Пример индекса для NumCompaniesWorked
            resume_on_job_search_site=row[13],  # Пример индекса для OverTime
            company_years_ratio=row[14],  # Пример индекса для PercentSalaryHike
            sent_messages=row[15],  # Пример индекса для TotalWorkingYears
            received_messages=row[16],  # Пример индекса для TrainingTimesLastYear
            message_recipients=row[17],  # Пример индекса для YearsAtCompany
            bcc_message_count=row[18],  # Пример индекса для YearsWithCurrManager
            cc_message_count=row[19],  # Пример индекса для SentMessages
            late_read_messages=row[20],  # Пример индекса для ReceivedMessages
            days_between_received_read=row[21],  # Пример индекса для AddressCount
            replied_messages=row[22],  # Пример индекса для BccCount
            sent_message_characters=row[23],  # Пример индекса для CcCount
            off_hours_sent_messages=row[24],  # Пример индекса для HoursToRead
            received_sent_ratio=row[25],  # Пример индекса для DaysBetweenReceiveRead
            received_sent_bytes_ratio=row[26],  # Пример индекса для RepliedMessages
            unanswered_questions=row[27],  # Пример индекса для OutgoingMessageLength
            probability=prediction(features_df)

        )
        db.add(new_feature)

    db.commit()

    return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)


@router.get("/export-csv")
async def export_csv(db: Session = Depends(get_db)):
    # Получаем данные из базы данных с учетом связанных объектов Feature
    result = db.execute(select(models.Employee).options(joinedload(models.Employee.features)))
    employees = result.unique().scalars().all()

    # Подготовка CSV файла
    output = StringIO()
    writer = csv.writer(output)

    # Заголовки столбцов
    writer.writerow([
        'department_id', 'surname', 'name', 'middlename', 'email',
        'age', 'education', 'marital_status', 'monthly_income', 'num_companies_worked',
        'over_time', 'total_working_years', 'years_at_company', 'resume_on_job_search_site',
        'company_years_ratio', 'sent_messages', 'received_messages', 'message_recipients',
        'bcc_message_count', 'cc_message_count', 'late_read_messages',
        'days_between_received_read', 'replied_messages', 'sent_message_characters',
        'off_hours_sent_messages', 'received_sent_ratio', 'received_sent_bytes_ratio',
        'unanswered_questions', 'probability'
    ])

    # Запись данных сотрудников и их характеристик в CSV
    for employee in employees:
        # Собираем данные о сотруднике
        employee_data = [employee.department_id, employee.surname, employee.name, employee.middlename, employee.email]

        # Для каждой записи характеристик сотрудника создаем отдельную строку в CSV
        if employee.features:
            for feature in employee.features:
                features_data = [
                    feature.age, feature.education, feature.marital_status, feature.monthly_income,
                    feature.num_companies_worked, feature.over_time, feature.total_working_years,
                    feature.years_at_company, feature.resume_on_job_search_site, feature.company_years_ratio,
                    feature.sent_messages, feature.received_messages, feature.message_recipients,
                    feature.bcc_message_count, feature.cc_message_count, feature.late_read_messages,
                    feature.days_between_received_read, feature.replied_messages, feature.sent_message_characters,
                    feature.off_hours_sent_messages, feature.received_sent_ratio, feature.received_sent_bytes_ratio,
                    feature.unanswered_questions, feature.probability
                ]
                writer.writerow(employee_data + features_data)
        else:
            # Если у сотрудника нет характеристик, создаем строку только с данными сотрудника
            writer.writerow(employee_data)

    output.seek(0)

    headers = {
        'Content-Disposition': 'attachment; filename="employees.csv"'
    }
    return StreamingResponse(iter([output.getvalue()]), media_type="text/csv", headers=headers)

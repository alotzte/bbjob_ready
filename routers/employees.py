import sys
import csv
sys.path.append("..")
import csv

from fastapi import Depends, APIRouter, Request, UploadFile, File
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

from .auth import get_current_user

from starlette.responses import RedirectResponse
from starlette import status

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

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
    reader = csv.reader(contents.decode().splitlines())

    next(reader, None)

    for row in reader:
        new_employee = models.Employee(
            department_id=row[0],  # Индекс столбца в CSV для department_id
            surname=row[1],        # Индекс столбца в CSV для surname
            name=row[2],           # Индекс столбца в CSV для name
            middlename=row[3],     # Индекс столбца в CSV для middlename
            email=row[4]           # Индекс столбца в CSV для email
        )
        db.add(new_employee)

    db.commit()

    return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)

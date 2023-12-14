import sys

sys.path.append("..")

from starlette import status
from starlette.responses import RedirectResponse
from fastapi import Depends, HTTPException, status, APIRouter, Request, Response, Form
import models
from database import SessionLocal, engine
from sqlalchemy.orm import Session
from pydantic import BaseModel
from .auth import get_current_user, verify_password, get_password_hash

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(
    prefix="/users",
    tags=["users"],
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


class UserVerification(BaseModel):
    username: str
    password: str
    new_password: str


@router.get("/edit-password", response_class=HTMLResponse)
async def change_password(request: Request):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)
    return templates.TemplateResponse("edit-user-password.html", {"request": request, "user": user})


@router.post("/edit-password")
async def change_password(request: Request, username: str = Form(...), old_password: str = Form(...),
                          new_password: str = Form(...),
                          db: Session = Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)

    user_data = db.query(models.Users).filter(models.Users.username == username).first()

    if user_data is not None:
        if username == user_data.username and verify_password(old_password, user_data.hashed_password):
            user_data.hashed_password = get_password_hash(new_password)
            db.commit()
            return templates.TemplateResponse("edit-user-password.html",
                                              {"request": request, "user": user, "msg": "Password changed successfully"})
    else:
        return templates.TemplateResponse("edit-user-password.html",
                                          {"request": request, "user": user, "msg": "Invalid username or password"})
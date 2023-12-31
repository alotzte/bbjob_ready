from fastapi import FastAPI
import models
from database import engine
from routers import auth, employees, users
from starlette.staticfiles import StaticFiles
from starlette import status
from starlette.responses import RedirectResponse


app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    return RedirectResponse(url="/employees", status_code=status.HTTP_302_FOUND)

app.include_router(employees.router)
app.include_router(auth.router)
app.include_router(users.router)

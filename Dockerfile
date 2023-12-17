FROM python:3.8

WORKDIR /app/server/

RUN pip install fastapi jinja2 uvicorn python-multipart websockets pandas SQLAlchemy psycopg2-binary passlib python-jose catboost

COPY . /app/server/

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0"]

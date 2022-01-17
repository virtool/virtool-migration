FROM python:3.8-slim
WORKDIR /migration
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN pip install psycopg2-binary
COPY ./alembic alembic
COPY ./alembic.ini .
CMD ["alembic", "upgrade", "head"]

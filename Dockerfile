FROM python:3.8-slim
WORKDIR /migration
RUN pip install poetry
COPY poetry.lock pyproject.toml ./
RUN poetry install
COPY ./revisions revisions
COPY ./alembic alembic
COPY ./alembic.ini .
COPY virtool_migration virtool_migration ./
CMD ["migration", "apply", "--alembic"]

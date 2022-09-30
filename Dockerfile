FROM python:3.8-slim as pip
WORKDIR /install
RUN pip install --user poetry==1.1.6
COPY pyproject.toml ./pyproject.toml
COPY poetry.lock ./poetry.lock
RUN /root/.local/bin/poetry export --dev > requirements.txt
RUN pip install --user -r requirements.txt

FROM python:3.8-slim
COPY --from=pip /root/.local /root/.local
COPY ./revisions revisions
COPY ./alembic alembic
COPY ./alembic.ini .
COPY ./virtool_migration virtool_migration
COPY pyproject.toml ./pyproject.toml
RUN pip install --user .
ENV PATH $PATH:/root/.local/bin
CMD ["migration", "apply", "--alembic"]

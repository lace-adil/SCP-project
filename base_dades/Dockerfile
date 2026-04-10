FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PYTHONIOENCODING=utf-8

RUN pip install --no-cache-dir poetry uvicorn
COPY ./app/pyproject.toml /root/app/pyproject.toml


WORKDIR /root/app

COPY ./app/pyproject.toml /root/app/pyproject.toml
RUN poetry install --no-root -v

ENTRYPOINT [ "/usr/local/bin/poetry", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080", "--reload" ]
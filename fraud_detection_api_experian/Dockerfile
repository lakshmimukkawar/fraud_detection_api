FROM python:3.8 as dev

RUN apt-get update
RUN pip3 install poetry


WORKDIR /src

COPY pyproject.toml ./

ENV PATH="${PATH}:/root/.poetry/bin"

RUN poetry config virtualenvs.create false

RUN poetry install --no-root

COPY . ./

WORKDIR /src

FROM dev as fraud_detection_api
EXPOSE 8000
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
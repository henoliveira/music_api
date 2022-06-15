FROM python:3.8.1-slim

COPY ./src /api/src
COPY ./env.py /api/env.py
COPY ./requirements.txt /api/requirements.txt

WORKDIR /api

RUN pip install -r requirements.txt

EXPOSE 8000:8000

CMD ["uvicorn", "src.main:api", "--host=0.0.0.0", "--reload"]
FROM python

WORKDIR /app


COPY . /app

RUN pip install -r requirements.txt

CMD uvicorn api.api:app --port=8000 --host=0.0.0.0
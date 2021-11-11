FROM python:3.10-alpine3.14
WORKDIR /app
RUN apk add --no-cache --update make
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . /app
CMD ["gunicorn", "server:app", "--bind", "0.0.0.0:5000"]

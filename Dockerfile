FROM python:3.8

WORKDIR /readvice_django

COPY . .
COPY requirements.txt requirements.txt

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

EXPOSE 8000
FROM python:3.7.1

WORKDIR /app

RUN pip install --upgrade pip
RUN pip install pipenv uwsgi

COPY Pipfile /app/Pipfile
COPY Pipfile.lock /app/Pipfile.lock
RUN pipenv install --system -d

COPY . /app

CMD ["python", "main.py"]
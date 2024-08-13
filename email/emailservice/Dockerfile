FROM python:3.11.1-bullseye

COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt


ENV LIBRD_VER=1.3.0

RUN pip install Pyrebase4
RUN pip install confluent_kafka

RUN pip install kafka-python
RUN pip install celery
RUN pip install redis

COPY . .

EXPOSE 8083
WORKDIR /usr/src/app

# CMD ["python", "manage.py", "makemigrations"]
# CMD ["python", "manage.py", "migrate"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8083"]
# CMD ["celery", "worker", "-A", "emailservice", "--loglevel=debug", "--concurrency=4"]

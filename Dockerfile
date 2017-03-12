FROM python:3.6-slim
COPY . .
EXPOSE 8000
RUN apt-get update && apt-get install -y --no-install-recommends build-essential python3-dev libffi-dev
RUN pip install -r requirements.txt
RUN python manage.py migrate
CMD python manage.py runserver 0.0.0.0:8000
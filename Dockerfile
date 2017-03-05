FROM python:3.6-slim
COPY . .
EXPOSE 8000
RUN pip install -r requirements.txt
RUN python manage.py migrate
CMD python manage.py runserver 0.0.0.0:8000
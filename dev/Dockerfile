FROM devolio/base
RUN mkdir /app
WORKDIR /app
ADD requirements.txt /app/
RUN pip install -r requirements.txt
ADD . /app/
EXPOSE 8000
CMD python manage.py migrate && make s2
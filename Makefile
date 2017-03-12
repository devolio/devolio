s: 
	./manage.py runserver

bd:
	docker build -t devolio/devolio

rd:
	docker run -d -p 8000:8000 devolio/devolio
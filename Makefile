s:
	node_modules/.bin/webpack -w & \
	./manage.py runserver

build:
	node_modules/.bin/webpack -p &&\
	node_modules/.bin/uglifyjs \
	shared/static/shared/js/app.js \
	-o shared/static/shared/js/app.js

bd:
	docker build -t devolio/devolio .

rd:
	docker run -d -p 8000:8000 devolio/devolio

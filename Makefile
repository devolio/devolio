default:
	cat Makefile

# Run server that doesn't depend on an internet conenction
offline:
	export MA_OFFLINE_DEV=True && ./manage.py runserver

# Run development server on 0.0.0.0:8000
serve:
	./manage.py runserver 0.0.0.0:8000

# Django shell
ds:
	docker-compose -f dev/compose.yml exec devolio python manage.py shell

# Build and minify JS
js:
	node_modules/.bin/webpack -p &&\
	node_modules/.bin/uglifyjs \
	shared/static/shared/js/app.js \
	-o shared/static/shared/js/app.js

# Docker stuff
# Build the base image found in dev/Dockerfile.base (devolio/base)
base:
	docker build -t devolio/base - < ./dev/Dockerfile.base

# Build the Devolio Django app itself (devolio/devolio)
build:
	docker-compose -f dev/compose.yml build #--no-cache

# Run the app image itself (devolio/devolio)
up:
	docker-compose -f dev/compose.yml up -d
	@echo "##### IMPORTANT COMMANDS #####"
	@echo "DevChat is successfully running in the background."
	@echo "Location: http://127.0.0.1:8000/"
	@echo "To follow the logs, type: make logs"
	@echo "To stop the server, type: make down"
	@echo "To use the django shell, type: make dj"
	@echo "To 'SSH' into the container, type: make shell"

run: base build up

down:
	docker-compose -f dev/compose.yml down

# logs from app inside docker
logs:
	docker-compose -f dev/compose.yml logs -f --tail="all"

# "ssh" into the container
shell:
	docker-compose -f dev/compose.yml exec devolio bash


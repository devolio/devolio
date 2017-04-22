# Run development server on localhost:8000
s:
	node_modules/.bin/webpack -w & \
	./manage.py runserver

# Run development server on 0.0.0.0:8000
s2:
	node_modules/.bin/webpack -w & \
	./manage.py runserver 0.0.0.0:8000

# Build and minify JS
build:
	node_modules/.bin/webpack -p &&\
	node_modules/.bin/uglifyjs \
	shared/static/shared/js/app.js \
	-o shared/static/shared/js/app.js

# Docker stuff
# Build the base image found in dev/Dockerfile.base (devolio/base)
build_base:
	docker build -t devolio/base - < ./dev/Dockerfile.base

# Build the Devolio Django app itself (devolio/devolio)
bd:
	docker build -f ./dev/Dockerfile -t devolio/devolio .

# Run the app image itself (devolio/devolio)
rd:
	docker run -d -p 8000:8000 --env-file ./dev/env -v ${PWD}:/app \
	--name devolio devolio/devolio

# Kill the devolio container
kd:
	docker kill devolio

# Build the base and app images
devolio: build_base bd

# logs from app inside docker
dl:
	docker logs devolio
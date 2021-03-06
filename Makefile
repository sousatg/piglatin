debug:
	docker-compose -f docker-compose.debug.yaml up --build

build:
	docker build -t piglatin-api /app

tests:
	docker-compose exec piglatin python -m unittest discover tests

push:
	doctl registry login
	docker tag piglatin-api registry.digitalocean.com/piglatin
	docker push registry.digitalocean.com/piglatin

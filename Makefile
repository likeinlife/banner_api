dc = docker compose
dcdev = $(dc) -f docker-compose-dev.yaml

env:
	cp sample.env .env

up:
	$(dc) up --build -d

downv:
	$(dc) down -v

down:
	$(dc) down

dev-up:
	$(dcdev) up --build -d

dev-downv:
	$(dcdev) down -v

dev-down:
	$(dcdev) down

freeze:
	poetry export -o requirements.txt --without-hashes

local-revision:
	alembic revision -m "$(name)" --autogenerate

revision:
	$(dcdev) exec -it banner_api alembic revision -m "$(name)" --autogenerate

upgrade:
	$(dcdev) exec -it banner_api alembic upgrade head

fill-db:
	$(dcdev) exec -it banner_api python cli.py $(count)

test:
	${dc} -f tests/docker-compose.yaml up --build --abort-on-container-exit --exit-code-from tests --attach tests

test-down:
	${dc} -f tests/docker-compose.yaml down -v

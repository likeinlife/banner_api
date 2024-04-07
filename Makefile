dc = docker compose
dcdev = $(dc) -f docker-compose-dev.yaml

up-dev:
	$(dcdev) up --build -d

down-dev:
	$(dcdev) down -v

freeze:
	poetry export -o requirements.txt --without-hashes

local-revision:
	alembic revision -m "$(name)" --autogenerate

dev-revision:
	$(dcdev) exec -it banner_api alembic revision -m "$(name)" --autogenerate

dev-upgrade:
	$(dcdev) exec -it banner_api alembic upgrade head
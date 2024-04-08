dc = docker compose
dcdev = $(dc) -f docker-compose-dev.yaml

up:
	$(dcdev) up --build -d

downv:
	$(dcdev) down -v

down:
	$(dcdev) down

freeze:
	poetry export -o requirements.txt --without-hashes

local-revision:
	alembic revision -m "$(name)" --autogenerate

revision:
	$(dcdev) exec -it banner_api alembic revision -m "$(name)" --autogenerate

upgrade:
	$(dcdev) exec -it banner_api alembic upgrade head
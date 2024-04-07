start:
	uvicorn banner_api.main:app --reload

revision:
	alembic revision -m "$(name)" --autogenerate
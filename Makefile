setup:
	@cp -n .env-example .env || echo ".env already exists, skipping copy."

start: setup
	docker compose up -d --build --force-recreate

stop:
	docker compose down

tests_u:
	docker compose run --rm --entrypoint="" -e PYTHONPATH=/app api pytest

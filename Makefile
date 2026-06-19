# Agnosticismo del Host - Todo corre dentro de Docker

.PHONY: up down build restart logs backend-shell db-shell test migration-check

up:
	docker compose up -d

down:
	docker compose down -v

build:
	docker compose build

restart:
	docker compose restart

logs:
	docker compose logs -f

backend-shell:
	docker compose exec backend sh

db-shell:
	docker compose exec db psql -U postgres -d crm_lead_management

test:
	docker compose exec backend pytest tests/ -v

migration-check:
	docker compose exec backend alembic current
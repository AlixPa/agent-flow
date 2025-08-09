ENV_FILE         ?= .env
COMPOSE           = docker compose --env-file $(ENV_FILE)
COMPOSE_LOG       = exec $(COMPOSE)
COMPOSE_UP_DETACH = $(COMPOSE) up -d

mysql:
	$(COMPOSE_UP_DETACH) --build mysql

migrator: mysql
	$(COMPOSE_LOG) up --build migrator

backend: migrator
	$(COMPOSE_LOG) up --build backend

backend-dev: migrator
	$(COMPOSE_LOG) watch backend

frontend:
	$(COMPOSE_LOG) up --build frontend

frontend-dev:
	$(COMPOSE_LOG) watch frontend

stop:
	$(COMPOSE_LOG) down

.PHONY: frontend frontend-dev stop backend backend-dev migrator mysql
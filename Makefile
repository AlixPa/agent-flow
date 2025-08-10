ENV_FILE         ?= .env
COMPOSE           = docker compose --env-file $(ENV_FILE)
COMPOSE_BUILD     = $(COMPOSE) build
COMPOSE_LOG       = exec $(COMPOSE)
COMPOSE_UP_DETACH = $(COMPOSE) up -d

mysql:
	$(COMPOSE_BUILD) mysql
	$(COMPOSE_UP_DETACH) mysql

migrator: mysql
	$(COMPOSE_BUILD) migrator
	$(COMPOSE_UP_DETACH) migrator

backend: migrator
	$(COMPOSE_BUILD) backend
	$(COMPOSE_UP_DETACH) backend

backend-dev: migrator
	$(COMPOSE_BUILD) backend
	$(COMPOSE_LOG) watch backend

frontend:
	$(COMPOSE_BUILD) frontend
	$(COMPOSE_UP_DETACH) frontend

frontend-dev:
	$(COMPOSE_BUILD) frontend
	$(COMPOSE_LOG) watch frontend

stop:
	$(COMPOSE_LOG) down

app: frontend backend

.PHONY: frontend frontend-dev stop backend backend-dev migrator mysql app
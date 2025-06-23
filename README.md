# Agent Flow

_As of 2025-06-21_

This repository is a work in progress. It will contain the code for a full-stack application.

## Description

A visual interface for building multi-agent AI workflows. Connect nodes, assign tools, and auto-generate runnable code.

## Details

The final application will include:

- A tab to create agent workflows: define agents by customizing base agents, assigning tools, and linking them together.
- A tab to run the created agent workflows.

Agent workflows are intended to be created and updated automatically via code generation logic.

# Runing the application

## Backend

### Simple run

Before running the application, you need to have Docker Desktop installed:

1. Download Docker Desktop from [https://www.docker.com/products/docker-desktop/](https://www.docker.com/products/docker-desktop/)
2. Install Docker Desktop following the installation instructions for your operating system
3. Start Docker Desktop and ensure it's running

---

Copy paste `.env-example` to `.env` and fill it with your own environment requirements (or leave default).

---

Then to run the backend, use the following command:

```bash
docker compose up -d --build backend
```

---

To stop the application, use the following command:

```bash
docker compose stop mysql backend
docker compose rm -f mysql backend migrator
```

---

The backend will be accessible at:

- API: http://127.0.0.1:8080/
- API Documentation: http://localhost:8080/docs
- Alternative API Documentation: http://localhost:8080/redoc

Note that 8080 is default port but you can change `BACKEND_PORT` in the .env file.
MySQL will be accessible at `MYSQL_PORT_LOCAL` (13306 by default)

### Manual run

Python version: Python 3.13.3

1. Install the `backend/requirements.txt` in a local environment
2. Run the backend

```bash
gunicorn main:app --workers 1 --k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8080
```

3. Access the backend at `127.0.0.1:8080/`

### To contribute

Create your local environment for this repo

```bash
python3.11 -m venv .venv
```

Activate it (bash/zsh)

```bash
source .venv/bin/activate
```

Install requirements

```bash
python -m pip install -r backend/requirements.txt
```

### Formating

Make sure you are in root folder of the repository

Then make sure to install and activate the extensions on your IDE

- black formatter
- isort

Note that you should make sure to have the same args in your isort and black formatter settings as in the `.pre-commit-config.yaml` file
![](images/pre_commit_config.png)
![](images/isort_settings.png)

Then, once venv is activated, make sure to install pre-commit with

```bash
pre-commit install
```

And voilà. Now everytime you try to commit it will reformat the files if you are not respecting the formatting of blackformatter and isort. But as you have the extensions on, everything should be fine.

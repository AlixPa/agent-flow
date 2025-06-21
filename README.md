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

Dockers soon available

## Backend

Python version: Python 3.13.3

For a simple local run

1. Install the requirements.txt in a local environment
2. Run the backend

```bash
gunicorn main:app --workers 3 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

3. Access the backend at `127.0.0.1:8000/`

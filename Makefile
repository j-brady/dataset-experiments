.PHONY: start firefox

SHELL := /bin/bash

uvicorn:
	uvicorn app:app --reload

firefox:
	firefox http://127.0.0.1:8000/table/id/lt/10

venv:
	python3.10 -m venv venv
	source venv/bin/activate && pip3 install --upgrade pip && pip install dataset pillow fastapi "uvicorn[standard]" pydantic ipython jinja2
	@echo Start your venv with 'source ./venv/bin/acivate' then 'make start'

install: venv

start: uvicorn 

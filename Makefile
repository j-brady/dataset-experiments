.PHONY: start firefox

SHELL := /bin/bash
venv = venv
activate = $(venv)/bin/activate

uvicorn:
	uvicorn app:app --reload 

open:
	firefox http://127.0.0.1:8000/table/id/lt/10

venv:
	python3.10 -m venv $(venv)
	source $(activate) && pip3 install --upgrade pip && pip install dataset pillow fastapi "uvicorn[standard]" pydantic ipython jinja2
	@echo Start your venv with 'source $(activate)' then 'make start'

dummydata:
	# create some dummy data
	source $(activate) && python db.py

install: venv dummydata uvicorn

start: uvicorn 

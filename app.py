import json
from pathlib import Path
from enum import Enum

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import table


from models import Dataset
from db import db

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


class Operator(Enum):
    startswith = "startswith"
    endswith = "endswith"
    gt = "gt"
    lt = "lt"
    gte = "gte"
    lte = "lte"
    isnot = "not"
    like = "like"
    ilike = "ilike"
    notlike = "notlike"


class Table(Enum):
    table = "table"


@app.get("/")
def read_root():
    datasets = []
    for dataset in db["table"]:
        datasets.append(dataset)
    return json.dumps(datasets)


@app.get("/{table}/findone/{column}/{value}", response_class=HTMLResponse)
def find_one(request: Request, table: Table, column: str, value: str):
    query = {column: eval(value)}
    dataset = db[table.value].find_one(**query)
    return templates.TemplateResponse(
        "item.html",
        {"dataset": dataset, "request": request, "id": column, "value": value},
    )


@app.get("/{table}/find/{column}/{value}", response_class=HTMLResponse)
def find(request: Request, table: Table, column: str, value: str):
    query = {column: eval(value)}
    print(table.value)
    datasets = db[table.value].find(**query)
    return templates.TemplateResponse(
        "items.html",
        {"datasets": datasets, "request": request, "id": column, "value": value},
    )


@app.get("/{table}/find/{column}/between/", response_class=HTMLResponse)
def find_between(
    request: Request, table: Table, column: str, mini: int = 1, maxi: int = 10
):
    """

    Example
    -------
    http://127.0.0.1:8000/find/data/between/?mini=1&maxi=5
    """
    if maxi < mini:
        mini, maxi = maxi, mini
    else:
        pass
    query = {column: {"between": [mini, maxi]}}
    datasets = db[table].find(**query)
    return templates.TemplateResponse(
        "items.html", {"datasets": datasets, "request": request}
    )


@app.get("/{table}/{column}/{operator}/{value}", response_class=HTMLResponse)
def find_operator(
    request: Request, table: Table, column: str, operator: Operator, value: str
):
    """

    Parameters
    ----------
    request: Request
    table: Table
        Enum with table names
    column: str
        column names (should also use Enum?)
    operator: Operator
        Enum with valid operators for interfacing with dataset api
    value: str
        value you wish to query your database with
    
    Example
    -------
    To get ids from "table" with values less than 10: 
    http://127.0.0.1:8000/table/id/lt/10

    To get names from

    """
    dic = {column: {operator.value: value}}
    datasets = db[table.value].find(**dic)
    return templates.TemplateResponse(
        "items.html", {"datasets": datasets, "request": request, "name": value}
    )


@app.get("/{table}/download/{id}", response_class=FileResponse)
def download_attachment(request: Request, table: Table, id: str):
    attachment = db[table].find_one(id=id).get("attachment")
    temp_file = Path("static/tmp.zip")
    if attachment is not None:
        temp_file.write_bytes(attachment)
        return temp_file

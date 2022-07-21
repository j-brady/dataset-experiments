import json
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse 
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


from models import Dataset
from db import db

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/")
def read_root():
    datasets = []
    for dataset in db["table"]:
        datasets.append(dataset)
    return json.dumps(datasets)

@app.get("/findone/{column}/{value}", response_class=HTMLResponse)
def find_one(request: Request, column: str, value: str):
    query = {column: eval(value)}
    dataset = db["table"].find_one(**query)
    return templates.TemplateResponse("item.html", {"dataset":dataset, "request": request, "id":column, "value": value})

@app.get("/find/{column}/{value}", response_class=HTMLResponse)
def find(request: Request, column: str, value: str):
    query = {column: eval(value)}
    datasets = db["table"].find(**query)
    return templates.TemplateResponse("items.html", {"datasets":datasets, "request": request, "id":column, "value": value})

@app.get("/find/{column}/between/", response_class=HTMLResponse)
def find_between(request: Request, column: str, mini: int=1, maxi: int=10):
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
    datasets = db["table"].find(**query)
    return templates.TemplateResponse("items.html", {"datasets":datasets, "request": request})

@app.get("/{column}/startswith/{query}", response_class=HTMLResponse)
def find_startswith(request: Request, column: str, query: str):
    dic = {column: {"startswith": query}}
    datasets = db["table"].find(**dic)
    return templates.TemplateResponse("items.html", {"datasets":datasets, "request": request, "name":query})

@app.get("/download/{id}", response_class=FileResponse)
def download_attachment(request: Request, id: str):
    attachment = db["table"].find_one(id=id).get("attachment")
    temp_file = Path("static/tmp.zip")
    if attachment is not None:
        temp_file.write_bytes(attachment) 
        return temp_file


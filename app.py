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


@app.get("/item/{id}", response_class=HTMLResponse)
def read_item(request: Request, id: str):
    
    dataset = db["table"].find_one(id=id)
    return templates.TemplateResponse("item.html", {"dataset":dataset, "request": request, "id":id})

@app.get("/item/{id_min}/{id_max}", response_class=HTMLResponse)
def read_range(request: Request, id_min: str, id_max: str):
    if id_max < id_min:
        id_min, id_max = id_max, id_min
    else:
        pass


@app.get("/contains/{name}", response_class=HTMLResponse)
def read_items(request: Request, name: str):
    datasets = db["table"].find(name={"startswith": name})
    return templates.TemplateResponse("items.html", {"datasets":datasets, "request": request, "name":name})

@app.get("/download/{id}", response_class=FileResponse)
def get_attachment(request: Request, id: str):
    attachment = db["table"].find_one(id=id).get("attachment")
    temp_file = Path("static/tmp.zip")
    if attachment is not None:
        temp_file.write_bytes(attachment) 
        return temp_file


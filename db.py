import random
from base64 import b64encode
from io import BytesIO
from zipfile import ZipFile

import dataset
from PIL import Image
from sqlalchemy import LargeBinary

from models import Dataset

db = dataset.connect("sqlite:///testdb.db")


def image_to_b64():
    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    img = Image.new("RGB", (60, 30), color=color)
    with BytesIO() as out:
        img.save(out, format="png")
        return b64encode(out.getvalue()).decode()


def zip_file():
    zf = BytesIO()
    with ZipFile(zf, "w") as myzip:
        myzip.write("./static/eggs.txt")
        myzip.write("./static/ham.txt")
    return zf.getvalue()


if __name__ == "__main__":
    table = db["table"]
    names = ["spam", "ham", "eggs"]
    len_names = len(names)
    for i in range(100):
        name = names[i % len_names]
        data = i
        img = image_to_b64()
        attach = zip_file()
        ds = Dataset(name=name, data=data, img=img, attachment=attach)
        table.insert(ds.dict(), types={"attachment": LargeBinary})

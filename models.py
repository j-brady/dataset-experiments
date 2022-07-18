from pydantic import BaseModel


class Dataset(BaseModel):
    name: str
    data: object
    img: object
    attachment: object

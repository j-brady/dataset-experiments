from pydantic import BaseModel


class Dataset(BaseModel):
    name: str
    data: int
    img: str  # base64 string
    attachment: bytes

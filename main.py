# Pythom
from typing import Optional

# Pydantic
from pydantic import BaseModel

# fastAPI
from fastapi import FastAPI, Body, Query


app = FastAPI()

# Models

class Person(BaseModel):
    first_name: str
    last_name: str
    age: int
    hair_color: Optional[str] = None # parametro opcional, si no se incluye se manda None
    is_married: Optional[bool] = None

@app.get("/")
def home():
    return {"Hello": "World again"}


# request and response body

@app.post("/person/new")
def create_person(person: Person = Body(...)): # el operador '...' indica que el parametro es obligatorio
    return person

# Validation

@app.get('/person/detail')
def show_person(
    name: Optional[str] = Query(None, min_length=1, max_length=50),
    age: int = Query(...)
):
    return {name: age}
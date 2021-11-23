from typing import Optional
from pydantic import BaseModel
from fastapi import FastAPI, Body

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

@app.post("/person/new")
def create_person(person: Person = Body(...)): # el operador '...' indica que el parametro es obligatorio
    return person

# Validation
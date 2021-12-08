# Pythom
from typing import Optional
from enum import Enum

# Pydantic
from pydantic import BaseModel, Field

# fastAPI
from fastapi import FastAPI, Body, Query, Path


app = FastAPI()

# Models

class HairColor(Enum):
    white = 'white'
    brown = 'brown'
    black = 'black'
    blonde = 'blonde'
    red = 'red'

class Location(BaseModel):
    city: str
    state: str
    country: str

class Person(BaseModel):
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
    )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
    )
    age: int = Field(
        ...,
        gt=0,
        le=115,
    )
    hair_color: Optional[HairColor] = Field(default=None) # parametro opcional, si no se incluye se manda None
    is_married: Optional[bool] = Field(default=None)

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
    name: Optional[str] = Query(
        None,
        min_length=1,
        max_length=50,
        title='Person Name',
        description='This is the person name.',
    ),
    age: int = Query(
        ...,
        title='Person age',
        description='This is the person age and is required'
    )
):
    return {name: age}


@app.get("/person/detail/{person_id}")
def show_person(
    person_id: int = Path(
        ...,
        gt=0,
    )
):
    return { person_id: 'It exists!' }

# Validation request body

@app.put("/person/{person_id}")
def update_person(
    person_id: int = Path(
        ...,
        title = 'Person id',
        description = 'This is the person ID',
        gt = 0,
    ),
    person: Person = Body(...),
    location: Location = Body(...),
):
    results = person.dict()
    results.update(location.dict())
    return results

    
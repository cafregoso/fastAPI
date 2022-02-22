# Pythom
from email import message
from email.errors import MessageError
from importlib.resources import path
from turtle import st
from typing import Optional
from enum import Enum

# Pydantic
from pydantic import BaseModel, Field

# fastAPI
from fastapi import FastAPI, Body, Query, Path, Form, status


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

class PersonBase(BaseModel):

    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example='Carlos'
    )

    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example='Alvarez'
    )

    age: int = Field(
        ...,
        gt=0,
        le=115,
        example=26
    )

    hair_color: Optional[HairColor] = Field(
        default=None, 
        example=HairColor.red,
    ) # parametro opcional, si no se incluye se manda None

    is_married: Optional[bool] = Field(
        default=None,
        example=False,
    )

class Person(PersonBase):
    password: str = Field(
        ...,
        min_length=8,
        example='passwordTest'
    )


class LoginOut(BaseModel):
    username: str = Field(
        ..., 
        max_length=30, 
        example='cafregoso',
    )
    message: str = Field(default='Login Succesfully!')


# PersonOut doesn't return password
class PersonOut(PersonBase):
    pass

@app.get(path='/', status_code=status.HTTP_200_OK)
def home():
    return {"Hello": "World again"}


# request and response body

@app.post(
    path='/person/new', 
    response_model=PersonOut,
    status_code=status.HTTP_201_CREATED,
)
def create_person(person: Person = Body(...)): # el operador '...' indica que el parametro es obligatorio
    return person

# Validation

@app.get(
    path='/person/detail',
    status_code=status.HTTP_200_OK,
)
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


@app.get(
    path="/person/detail/{person_id}",
    status_code=status.HTTP_200_OK,
)
def show_person(
    person_id: int = Path(
        ...,
        gt=0,
    )
):
    return { person_id: 'It exists!' }

# Validation request body

@app.put(
    path="/person/{person_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def update_person(
    person_id: int = Path(
        ...,
        title = 'Person id',
        description = 'This is the person ID',
        gt = 0,
    ),
    person: Person = Body(...),
    # location: Location = Body(...),
):
    # results = person.dict()
    # results.update(location.dict())
    return person

#Formularios

@app.post(
    path='/login',
    response_model=LoginOut,
    status_code=status.HTTP_200_OK,
)
def login(
    username: str = Form(...),
    password: str = Form(...),
):
    return LoginOut(username=username)
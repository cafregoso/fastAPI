# Python
from typing import Optional
from enum import Enum

# Pydantic
from pydantic import BaseModel, Field, EmailStr

# fastAPI
from fastapi import FastAPI
from fastapi import status
from fastapi import HTTPException
from fastapi import Body, File, Header, Query, Path, Form, UploadFile, Header, Cookie


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

@app.get(
    path='/', 
    status_code=status.HTTP_200_OK,
    tags=['Home'],
)
def home():
    """
        
    """
    return {"Hello": "World again"}


# request and response body

@app.post(
    path='/person/new', 
    response_model=PersonOut,
    status_code=status.HTTP_201_CREATED,
    tags=['Persons'],
)
def create_person(person: Person = Body(...)): # el operador '...' indica que el parametro es obligatorio
    return person

# Validation

@app.get(
    path='/person/detail',
    status_code=status.HTTP_200_OK,
    tags=['Persons'],
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

persons = [1, 2, 3, 4, 5]

@app.get(
    path="/person/detail/{person_id}",
    status_code=status.HTTP_200_OK,
    tags=['Persons'],
)
def show_person(
    person_id: int = Path(
        ...,
        gt=0,
        example=123
    )
):
    if person_id not in persons:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This person doesn't exist!"
        )

    return { person_id: 'It exists!' }

# Validation request body

@app.put(
    path="/person/{person_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=['Persons'],
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
    tags=['Persons'],
)
def login(
    username: str = Form(...),
    password: str = Form(...),
):
    return LoginOut(username=username)

# Cookies and Headers Parameters
@app.post(
    path='/contact',
    status_code=status.HTTP_200_OK,
    tags=['Contact']
)
def contact(
    first_name: str = Form(
        ...,
        max_length=30,
        min_length=2,
    ),
    last_name: str = Form(
        ...,
        max_length=30,
        min_length=2,
    ),
    email: EmailStr = Form(...),
    message: str = Form(
        ...,
        min_length=20,
    ),
    user_agent: Optional[str] = Header(default=None),
    ads: Optional[str] = Cookie(default=None),
):
    return user_agent

@app.post(
    path="/post-image",
    tags=['Media']
)
def post_image(
    image: UploadFile = File(...)
):
    return {
        "Filename": image.filename,
        "Format": image.content_type, 
        "Size(kb)": round(len(image.file.read()) / 1024, ndigits=2)
    }
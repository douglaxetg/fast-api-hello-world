#Python
from typing import Optional
from enum import Enum

#Pydantic
from pydantic import BaseModel
from pydantic import Field

#FastAPI
from fastapi import FastAPI, Body, Query, Path, status

app = FastAPI()

class HairColor(Enum):
    white = "white"
    brown = "brown"
    black = "black"
    yellow = "yellow"
    red = "red"

class Location(BaseModel):
    city: str
    state: str
    country: str

class PersonBase(BaseModel):
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example="Douglas"
        )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example="Tovar"
    )
    age: int = Field(
        ...,
        gt=0,
        le=115,
        example=42
    )
    hair_color: Optional[HairColor] = Field(default=None, example=HairColor.black)
    is_married: Optional[bool] = Field(default=None, example=False)
    
class Person(PersonBase):
    password: str = Field(..., min_length=8)
    
class PersonOut(PersonBase):
    pass
    
@app.get(
    path="/",
    status_code=status.HTTP_200_OK
    )
def home():
    return {"hello":"World"}

#Request and Response Body
@app.post(
    path="/person/new",
    response_model=PersonOut,
    status_code=status.HTTP_201_CREATED
    )
def create_person(person: Person = Body(...)):
    return person
    
@app.get(
    path="/person/detail",
    status_code=status.HTTP_200_OK
    )
def show_person(
    name: Optional[str] = Query(
        None, 
        min_length=1, 
        max_length=50,
        title="Person Name",
        description="This is the person name, It's between 1 and 50 characters",
        example="Rocio"
        ),
    age: str = Query(
        ...,
        title="Person Age",
        description="This is the person Age. It's required",
        example=25
        )
):
    return {name: age}

@app.get("/person/detail/{person_id}")
def show_person(
    person_id: int = Path(
        ...,
        gt=0,
        example=123
        )
):
    return {person_id: "It exist!"}


@app.put("/person/{person_id}")
def update_person(
    person_id: int = Path(
        ...,
        title="Person ID",
        description="This is the poerson ID",
        gt=0,
        example=123
    ),
    person: Person = Body(...),
    # location: Location = Body(...)
):
    # results = person.dict()
    # results.update(location.dict())
    return person
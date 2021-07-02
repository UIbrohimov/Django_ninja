import random

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from ninja import File, Form, NinjaAPI, Path
from ninja.files import UploadedFile
from typing import List

from .models import Employee, Task
from .schema import (
    EmployeeOut, EmployeeIn, userOut,
    userIn, Item, PathDate, TaskSchema
)


api = NinjaAPI()


# basic math with Inshteyn
@api.get("/add")
def add(request, a: int, b: int):
    return {"result": a + b}


@api.get("/items/{item_id}")
def read_item(request, item_id: int):
    return {"item_id": item_id}


# Playing with api (generating a walid date)
@api.get("/events/{year}-{month}-{day}")
def events(request, date: PathDate = Path(...)):
    return {"date": date.value()}


# playing with api
weapons = [
    "Ninjato", "Shuriken", "Katana", "Kama", "Kunai", "Naginata", "Yari"
]


@api.get("/weapons")
def list_weapons(request, limit: int = 10, offset: int = 0):
    return weapons[offset: offset + limit]


# Implementing search
@api.get("/weapons/search")
def search_weapons(request, q: str, offset: int = 0):
    results = [w for w in weapons if q in w.lower()]
    return {"results": results}


# shema with path parameters
@api.post("/items")
def event_s(request, item_id, item: Item, q: str):
    return {"item_id": item_id, "item": item.dict(), "q": q}


# form fields transaction
@api.post("/login")
def login(request, username: str = Form(...), password: str = Form(...)):
    return {"username": username, "password": "*******"}


# Uploading a file


@api.post("/upload")
def upload(request, file: UploadedFile = File(...)):
    return {
        "name": file.name,
        "size": str(file.size) + " byte",
        "file type": file.content_type.split("/")[1],
    }


# uploading more than one file
@api.post("/upload-pultiple")
def multiple_upload(request, files: List[UploadedFile] = File(...)):
    return [file.name for file in files]


@api.post("/users/", response=userOut)
def create_user(request, data: userIn):
    user = User(username=data.username)  # User is django auth.User
    user.set_password(data.password)
    user.save()
    return user


@api.get("/tasks", response=List[TaskSchema])
def tasks(request):
    return Task.objects.all()


# creating an object with django ninja
@api.post("/employees", response=EmployeeOut)
def create_employee(request, payload: EmployeeIn):
    employee = Employee.objects.create(**payload.dict())
    return employee


# retrieve a certain object
@api.get("/employees/{employee_id}", response=EmployeeOut)
def get_employee(request, employee_id: int):
    employee = get_object_or_404(Employee, id=employee_id)
    return employee


# retrieving all objects with django ninja
@api.get("/employees", response=List[EmployeeOut])
def employees(request):
    employees = Employee.objects.all()
    return employees


# updating an employee object
@api.put("/employees/{employee_id}", response=EmployeeOut)
def update_employee(request, employee_id: int, payload: EmployeeIn):
    employee = get_object_or_404(Employee, id=employee_id)
    for attr, value in payload.dict().items():
        setattr(employee, attr, value)
    employee.save()
    return employee


# deleting an employee from the db
@api.delete("/employees/{employee_id}")
def delete_employee(request, employee_id: int):
    employee = get_object_or_404(Employee, id=employee_id)
    employee.delete()
    return {"success": True}


class ServiceUnavailableError(Exception):
    pass


# initializing handler


@api.exception_handler(ServiceUnavailableError)
def service_unavailable(request, exc):
    return api.create_response(
        request,
        {"message": "Please retry later"},
        status=503,
    )


# some logic that throws exception


@api.get("/service", description="this is what you want")
def some_operation(request):
    if random.choice([True, False]):
        raise ServiceUnavailableError()
    return {"message": "Hello"}

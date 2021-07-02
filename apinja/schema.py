import datetime

from ninja import Schema


class userIn(Schema):
    username: str
    password: str


class userOut(Schema):
    id: int
    username: str


# creating a schema
class Item(Schema):
    name: str
    description: str = None
    price: float
    quantity: int


# extraction date items
class PathDate(Schema):
    year: int
    month: int
    day: int

    def value(self):
        return datetime.date(self.year, self.month, self.day)


# task for the user
class TaskSchema(Schema):
    id: int
    title: str
    is_completed: bool
    owner: userOut = None


class EmployeeIn(Schema):
    first_name: str
    last_name: str
    department_id: int = None
    birthdate: datetime.date = None


class EmployeeOut(Schema):
    id: int
    first_name: str
    last_name: str
    department_id: int = None
    birthdate: datetime.date = None

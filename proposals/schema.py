from ninja.orm import create_schema

from .models import Project, Task

TaskSchema = create_schema(Task)
ProjectSchema = create_schema(Project)

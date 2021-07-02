from typing import List

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from ninja import Router

from proposals.models import Project, Task

from .schema import ProjectSchema, TaskSchema


router = Router(tags=["Proposals App"])


@router.get(
    "/project/{project_id}/tasks/",
    response=List[TaskSchema]
)
def task_list(request):
    try:
        user_projects = request.user.project_set
        project = get_object_or_404(
            user_projects, id=request.GET.get("project_id")
        )
        return project.task_set.all()
    except Exception as e:
        print(e)
        return Task.objects.all()


@router.get(
    "/project/{project_id}/tasks/{task_id}/",
    response=TaskSchema
)
def details(request, task_id: int):
    try:
        user_projects = request.user.project_set
        project = get_object_or_404(
            user_projects, id=request.GET.get("project_id")
        )
        user_tasks = project.task_set.all()
        return get_object_or_404(user_tasks, id=task_id)
    except Exception as e:
        print(e)
        return Task.objects.get(id=task_id)


@router.post(
    "/project/{project_id}/tasks/{task_id}/complete",
    response=TaskSchema
)
def complete(request, task_id: int):
    try:
        user_projects = request.user.project_set
        project = get_object_or_404(
            user_projects, id=request.GET.get("project_id")
        )
        user_tasks = project.task_set.all()
        task = get_object_or_404(user_tasks, id=task_id)
        task.completed = True
        task.save()
        return task
    except Exception as e:
        print(e)
        return Task.objects.get(id=task_id)


@router.post("/create-task", response=TaskSchema)
def create_task(request, payload: TaskSchema):
    data = payload.dict()
    # print(data)
    project = get_object_or_404(Project, id=data["project"])
    task = Task.objects.create(
        project=project,
        title=data["title"],
        completed=data["completed"]
    )
    return task


@router.post("/create-project", response=ProjectSchema)
def create_project(request, payload: ProjectSchema):
    data = payload.dict()
    owner = get_object_or_404(User, id=data["owner"])
    obj = Project.objects.create(
        title=data["title"], owner=owner
    )
    return obj

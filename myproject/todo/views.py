import dataclasses
from typing import List

from django.http import JsonResponse, HttpRequest, HttpResponseNotAllowed, HttpResponseNotFound, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .models import TodoDbModel, UserDbModel
from django.http import QueryDict


# Create your views here.
def index_json(request):
    return JsonResponse({
        "greet": "Hello World!"
    })


@csrf_exempt
def sign_up(request: HttpRequest):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    username: str = request.POST["username"]
    password: str = request.POST["password"]

    try:
        db_user = UserDbModel.objects.get(username=f"{username}")
        if db_user.username == username:
            return JsonResponse({
                "cause": "username"
            }, status=409)
    except UserDbModel.DoesNotExist:
        new_user: UserDbModel = UserDbModel(
            username=username,
            password=password
        )
        new_user.save()

        return JsonResponse({
            "user_id": new_user.pk
        })


@csrf_exempt
def log_in(request: HttpRequest):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    username = request.POST['username']
    password = request.POST['password']

    db_user: UserDbModel = UserDbModel.objects.get(username=f"{username}")
    if username == db_user.username:
        if password == db_user.password:
            return JsonResponse({
                "user_id": db_user.pk
            })

        return JsonResponse({
            "cause": "password"
        }, status=401)

    return JsonResponse({
        "cause": "username"
    }, status=401)


def check_todo_list(request: HttpRequest, user_id: int):
    user_model: UserDbModel = UserDbModel.objects.get(pk=user_id)
    todo_model_list: List[TodoDbModel] = [todo_list for todo_list in user_model.tododbmodel_set.all()]
    user_todo_list = []
    for todo_model in todo_model_list:
        todo_dict = convert_todo_model_to_dict(todo_model)
        user_todo_list.append(todo_dict)
    return JsonResponse({
        "todos": user_todo_list
    })


def convert_todo_model_to_dict(todo_model: TodoDbModel):
    return {
        'id': todo_model.pk,
        'title': todo_model.title,
        'status': todo_model.status
    }

sessions = {
    "35873874": {
        "my_car": "porsche"
    },
    "348273487": {
        "my_car": "toyota"
    }
}

@csrf_exempt
def create_new_todo(request: HttpRequest, user_id: int):
    previously_selected_car = request.session["my_car"]

    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    title = request.POST['title']
    status = request.POST['status']
    user_id = user_id

    new_todo: TodoDbModel = TodoDbModel(
        title=title,
        status=status,
        user_id=user_id,
    )

    new_todo.save()
    return JsonResponse(convert_todo_model_to_dict(new_todo))


@csrf_exempt
def modify_todo(request: HttpRequest, user_id: int, todo_id: int):
    if request.method != "PATCH":
        return HttpResponseNotAllowed(["PATCH"])


    request.session["soo"]
    update_todo: TodoDbModel = TodoDbModel.objects.get(pk=todo_id)

    data = QueryDict(request.body)
    for key, value in data.items():
        if key == 'title':
            update_todo.title = value
        elif key == 'status':
            update_todo.status = value

    update_todo.save()
    update_todo_dict = convert_todo_model_to_dict(update_todo)

    return JsonResponse(update_todo_dict)


@csrf_exempt
def delete_todo(request: HttpRequest, user_id: int, todo_id: int):
    if request.method != "DELETE":
        return HttpResponseNotAllowed(["DELETE"])

    try:
        todo_item = TodoDbModel.objects.get(pk=todo_id)
        todo_item.delete()
        return HttpResponse(status=200)
    except TodoDbModel.DoesNotExist:
        return HttpResponseNotFound()

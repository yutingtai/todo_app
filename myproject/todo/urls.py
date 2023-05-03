from django.urls import path
from . import views

app_name = "todo"
urlpatterns = [
    path("", views.index_json, name="index"),
    path("sign-up", views.sign_up, name="sign-up"),
    path("log-in", views.log_in, name="login"),
    path("todos/<int:user_id>", views.check_todo_list, name="todos"),
    path("create_new_todo/<int:user_id>", views.create_new_todo, name="create_new_todo"),
    path("modify_todo/<int:user_id>/<int:todo_id>", views.modify_todo, name="modify_todo"),
    path("delete_todo/<int:user_id>/todos/<int:todo_id>", views.delete_todo, name="delete_todo"),
]

